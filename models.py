from sqlalchemy import Column, Integer, String, Float
from database import Base

class Pipe(Base):
    __tablename__ = "pipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    length = Column(Float)
    diameter = Column(Float)
    status = Column(String)