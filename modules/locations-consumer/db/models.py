from sqlalchemy import Column, Integer, DateTime, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, nullable=False)
    coordinate = Column(Geometry("POINT", spatial_index=True), nullable=False) 
    creation_time = Column(DateTime, default=datetime.utcnow)