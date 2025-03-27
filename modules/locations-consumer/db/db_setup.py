from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from config import Config 


DATABASE_URL = "postgresql://user:password@db_host:5432/mydb"

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Creates tables if they don’t exist."""
    Base.metadata.create_all(bind=engine)