# Pipe Integrity Storage System

Простая подсистема хранения данных для системы контроля целостности труб. Реализована с помощью FastAPI и SQLite.

## Возможности

- Добавление труб
- Получение списка труб
- Удаление труб по ID

## Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/yourusername/pipe-integrity-system.git
cd pipe-integrity-system
```
2. Установи зависимости:

```bash
pip install -r requirements.txt
```
## Запуск сервера

```bash
uvicorn main:app --reload
```

## Открой в браузере:

```bash
http://127.0.0.1:8000/docs
```


## Примеры запросов (через curl)

Получить список труб
```
curl http://127.0.0.1:8000/pipes
```

Добавить трубу

```
curl -X POST "http://127.0.0.1:8000/pipes?name=MainPipe&length=120.5&diameter=30.2&status=ok"
```

Удалить трубу

```
curl -X DELETE http://127.0.0.1:8000/pipes/1
```

Загрузка труб из JSON-файла

```
curl -X POST "http://127.0.0.1:8000/pipes/upload_json" ^
  -F "file=@pipes.json;type=application/json"
```
## Зависимости
- FastAPI
- SQLAlchemy
- Uvicorn