from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi import File, UploadFile
import json
import models

# Создаём таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость: получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Pipe Integrity System"}

@app.get("/pipes")
def list_pipes(db: Session = Depends(get_db)):
    return db.query(models.Pipe).all()

@app.post("/pipes")
def add_pipe(name: str, length: float, diameter: float, status: str, db: Session = Depends(get_db)):
    pipe = models.Pipe(name=name, length=length, diameter=diameter, status=status)
    db.add(pipe)
    db.commit()
    db.refresh(pipe)
    return pipe

@app.delete("/pipes/{pipe_id}")
def delete_pipe(pipe_id: int, db: Session = Depends(get_db)):
    pipe = db.query(models.Pipe).filter(models.Pipe.id == pipe_id).first()
    if not pipe:
        raise HTTPException(status_code=404, detail="Pipe not found")
    db.delete(pipe)
    db.commit()
    return {"message": f"Pipe {pipe_id} deleted"}

@app.post("/pipes/upload_json")
async def upload_pipes_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON files are supported")

    contents = await file.read()
    try:
        pipes_data = json.loads(contents)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    if not isinstance(pipes_data, list):
        raise HTTPException(status_code=400, detail="JSON should be a list of pipes")

    added_pipes = []
    for pipe in pipes_data:
        try:
            name = pipe["name"]
            length = float(pipe["length"])
            diameter = float(pipe["diameter"])
            status = pipe["status"]
        except (KeyError, ValueError, TypeError):
            continue  # пропускаем некорректные записи

        new_pipe = models.Pipe(name=name, length=length, diameter=diameter, status=status)
        db.add(new_pipe)
        added_pipes.append(new_pipe)

    db.commit()
    return {"added": len(added_pipes)}