import logging
from db.db_setup import SessionLocal
from db.models import Location
from datetime import datetime
from config import Config
from geoalchemy2.elements import WKTElement

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("kafka-consumer")

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def save_location_to_db(data):
    """Save location data to the database."""
    session = SessionLocal()
    try:
        # Validate the incoming data
        if "person_id" in data and "latitude" in data and "longitude" in data and "creation_time" in data:
            
            # Creating a Point geometry using GeoAlchemy2
            point = WKTElement(f"POINT({data['longitude']} {data['latitude']})", srid=4326)

            # Parse the 'creation_time' with the correct format
            mytime = datetime.strptime(data["creation_time"], DATE_FORMAT)
            
            new_location = Location(
                person_id=data["person_id"],
                coordinate=point,  # Use the point geometry directly here
                creation_time=mytime 
            )

            session.add(new_location)
            session.commit()
            logger.info(f"Saved location to DB for person {new_location.person_id}")
        else:
            logger.error("Invalid data format received. Missing required fields.")
    except Exception as e:
        session.rollback()  # Rollback in case of error
        logger.error(f"Error saving to DB: {e}")
    finally:
        session.close()