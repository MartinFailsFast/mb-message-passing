from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from db.models import Base
from config import Config 
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def init_db(max_retries=Config.MAX_RETRIES, base_delay=Config.RETRY_INTERVAL):
    """Creates tables if they don’t exist, with retry on failure."""
    attempt = 0
    while attempt < max_retries:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully.")
            return
        except OperationalError as e:
            attempt += 1
            wait_time = base_delay * (2 ** (attempt - 1))  # Exponential backoff
            logger.warning(f"Database connection failed ({attempt}/{max_retries}): {e}")
            logger.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    logger.error("Failed to initialize database after multiple attempts.")