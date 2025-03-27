import os
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, NoBrokersAvailable
import json
import logging
import time
from flask import current_app
from typing import Optional
import traceback
from app.udaconnect.services import ConnectionService, LocationService
from app.udaconnect.models import Location
#from flask import Flask, current_app
from app import create_app 

# Get Kafka server from environment (set by Docker Compose)
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC_NAME = os.getenv('KAFKA_TOPIC', 'location-topic')




logging.basicConfig(level=logging.DEBUG)
logging.getLogger('kafka').setLevel(logging.WARNING)
logger = logging.getLogger("udaconnect-srv")

# Dictionary to temporarily store locations
locations = {}

def get_app():
    from app import app
    return app



def process_message(location_data: dict) -> Optional[Location]:

    try:
        app = create_app()
        with app.app_context():  # <-- Push app context here 
            logger.info(f"Prepare DB Insert message: {location_data}")
            location: Location = LocationService.create(location_data)

            logger.info(f"Created location: {location}")
            return location

    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error creating location: {e}\n{traceback.format_exc()}")
        return None

  
# Check if Kafka is ready by trying to connect to the broker
def is_kafka_ready():
    try:
        # Try connecting to Kafka broker without specifying a topic
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_SERVER,  # Kafka broker address in Docker
            group_id='location-consumer-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            consumer_timeout_ms=1000  # Timeout for consumer connection
        )
        # If no exception is raised, Kafka is available
        consumer.close()
        logging.debug("Kafka connection successful.")
        return True
    except NoBrokersAvailable:
        logging.warning("Kafka is not available yet. Retrying...")
        return False
    except Exception as e:
        logging.warning(f"Kafka connection failed with error: {e}. Retrying...")
        return False

# Create a Kafka producer to send location data
def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages as JSON
    )

#   Create a Kafka consumer to read location data
def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_SERVER,
        group_id='location-consumer-group',
        auto_offset_reset='earliest',  # Read from the beginning if no offset
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize JSON value
    )
# Send location data to Kafka
def send_location_to_kafka(location_data):
    producer = create_producer()
    try:
        producer.send(TOPIC_NAME, location_data)
        producer.flush()  # Ensure the message is sent before returning
        logging.debug(f"Kafka message produced: {location_data}")
    except BaseException as e:
        logging.error(f"Error producing message: {e}")

'''
# Simulate creating a new location from the Kafka message
def process_message(location_data: dict) -> Optional[Location]:
    try:
        logger.info(f"Perpare DB Insert message: {location_data}")
        #location_json = location_data.get_json(location_data)
        location: Location = LocationService.create(location_data)

        
        location_obj = Location(
            person_id=location_data.get('person_id'),
            longitude=str(location_data.get('longitude')),
            latitude=str(location_data.get('latitude')),
            creation_time=location_data.get('creation_time'),
        )
       
        location = LocationService.create(location_obj)
        

        logger.info(f"Created location: {location}")
        return location

    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error creating location: {e}\n{traceback.format_exc()}")
        return None
'''



# Consume location messages from Kafka
def consume_location_from_kafka():
    consumer = create_consumer()
    logger.info("Kafka consumer started and waiting for messages...")

    for message in consumer:
        if not message.value:
            logger.warning("Received empty message from Kafka")
            continue
        
        try:
            message_value = message.value
            logger.debug(f"Received Kafka message: {message_value}")

            location = process_message(message_value)

            if location:
                logger.info(f"Successfully processed message and created location: {location}")
            else:
                logger.error(f"Failed to process message: {message_value}")
        
        except Exception as e:
            logger.error(f"Error processing Kafka message: {e}")

def consume_location_from_kafkafail():
    consumer = create_consumer()
    logger.info("Kafka consumer started and waiting for messages...")

    # Ensure Flask app context is active
    with current_app.app_context():
        for message in consumer:
            if not message.value:
                logger.warning("Received empty message from Kafka")
                continue

            try:
                message_value = message.value
                logger.debug(f"Received Kafka message: {message_value}")

                # Call the process_message function (now works!)
                location = process_message(message_value)

                if location:
                    logger.info(f"Successfully processed message and created location: {location}")
                else:
                    logger.error(f"Failed to process message: {message_value}")

            except Exception as e:
                logger.error(f"Error processing Kafka message: {e}")



def consume_location_from_kafkanew():
    consumer = create_consumer()
    logger.info("Kafka consumer started and waiting for messages...")

    # Manuell den Flask-Kontext setzen
    with current_app.app_context():
        for message in consumer:
            if not message.value:
                logger.warning("Received empty message from Kafka")
                continue

            try:
                message_value = message.value
                logger.debug(f"Received Kafka message: {message_value}")

                # Call the process_message function (now works!)
                location = process_message(message_value)

                if location:
                    logger.info(f"Successfully processed message and created location: {location}")
                else:
                    logger.error(f"Failed to process message: {message_value}")

            except Exception as e:
                logger.error(f"Error processing Kafka message: {e}")


# Create Kafka AdminClient to check or create topics
def check_or_create_topicOld():
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_SERVER,
            client_id='location_service_admin'
        )


        existing_topics = admin_client.list_topics()
        if TOPIC_NAME not in existing_topics:
            logging.debug(f"Creating topic '{TOPIC_NAME}'...")
            topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)
            admin_client.create_topics(new_topics=[topic])
            logging.debug(f"Topic '{TOPIC_NAME}' created successfully on {KAFKA_SERVER}")
        else:
            logging.debug(f"Topic '{TOPIC_NAME}' already exists on {KAFKA_SERVER}")
        
        return True
    except NoBrokersAvailable:
        logging.warning("Kafka is not available yet. Retrying...")
        return False
    except KafkaError as e:
        logging.debug(f"Warning: Kafka error occurred: {e}. Retrying...")
        return False
    
def check_or_create_topic():
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_SERVER,
            client_id='location_service_admin'
        )

        # Get existing topics as a set
        existing_topics = set(admin_client.list_topics())
        if TOPIC_NAME not in existing_topics:
            logging.debug(f"Creating topic '{TOPIC_NAME}' on {KAFKA_SERVER}")
            topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)
            try:
                admin_client.create_topics(new_topics=[topic])
                logging.debug(f"Topic '{TOPIC_NAME}' created successfully.")
            except KafkaError as e:
                logging.error(f"Error creating topic '{TOPIC_NAME}': {e}")
                return False
        else:
            logging.debug(f"Topic '{TOPIC_NAME}' already exists on {KAFKA_SERVER}")
        
        logging.debug("Kafka Producer connection successful.")
        return True
    except NoBrokersAvailable:
        logging.warning("Kafka is not available yet. Retrying...")
        return False
    except KafkaError as e:
        logging.error(f"Kafka error occurred: {e}. Retrying...")
        return False