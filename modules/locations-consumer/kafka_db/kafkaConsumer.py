import json
import logging
import threading
import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from db.db_setup import SessionLocal
from db.models import Location
from db.services import save_location_to_db
from datetime import datetime
from config import Config
from geoalchemy2.elements import WKTElement

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("kafka-consumer")
logging.getLogger('kafka').setLevel(logging.WARNING)

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"




def connect_kafka_with_retry(max_retries=Config.MAX_RETRIES, initial_delay=Config.RETRY_INTERVAL):
    retries = 0
    while retries < max_retries:
        try:
                        # Log the parameters before creating the KafkaConsumer
            logger.debug(f"Attempting to create Kafka consumer with the following parameters:")
            logger.debug(f"KAFKA_TOPIC: {Config.KAFKA_TOPIC}")
            logger.debug(f"KAFKA_SERVER: {Config.KAFKA_SERVER}")
            logger.debug(f"KAFKA_CONSUMER_GROUP: {Config.KAFKA_CONSUMER_GROUP}")
            logger.debug(f"Value deserializer: json.loads(x.decode('utf-8'))")
            logger.debug(f"Auto offset reset: earliest")
            
            consumer = create_consumer()
            
            logger.info("Consumer connected to Kafka successfully.")
            return consumer
        except KafkaError as e:
            logger.error(f"Kafka connection failed (attempt {retries + 1}): {e}")
            retries += 1
            wait_time = initial_delay * (2 ** retries)  # Exponential backoff
            logger.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    logger.critical("Consumer could not connect to Kafka. Exiting...")
    exit(1)

def save_location_to_dbold(data):
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


def consume_location_from_kafka():
    consumer = connect_kafka_with_retry()
    logger.info("Kafka consumer started and waiting for messages...")

    while True:
        messages = consumer.poll(timeout_ms=1000) 
        if not messages:
            continue

        for _, records in messages.items():
            for message in records:
                try:
                    message_value = message.value
                    logger.debug(f"Received Kafka message: {message_value}")
                    # Call DB Script to persist data
                    save_location_to_db(message_value) 
                except Exception as e:
                    logger.error(f"Error processing Kafka message: {e}")

def create_consumer():
    return KafkaConsumer(
        Config.KAFKA_TOPIC,
        bootstrap_servers=Config.KAFKA_SERVER,
        group_id=Config.KAFKA_CONSUMER_GROUP,
        auto_offset_reset='earliest', #"latest" # Read from the beginning if no offset
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Deserialize JSON value
        session_timeout_ms=45000,  # Increase session timeout (default ~45s)
        heartbeat_interval_ms=15000,  # Send heartbeats every 15s
    )



def start_consumer():
    logger.debug("Starting Kafka consumer process...")

    # Start the consumer thread
    kafka_thread = threading.Thread(target=consume_location_from_kafka, daemon=False)  # DO NOT use daemon=True
    kafka_thread.start()
    
    logger.info("Kafka consumer thread started and running.")

    # Keep the main thread alive
    kafka_thread.join()  # This ensures the container does not exit
