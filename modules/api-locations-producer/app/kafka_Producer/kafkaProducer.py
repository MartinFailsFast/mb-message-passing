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
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka:9092')  # Default to localhost:9092
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'location-topic')  # Default topic name
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'location-consumer-group')  # Default group



logging.basicConfig(level=logging.DEBUG)
logging.getLogger('kafka').setLevel(logging.WARNING)
logger = logging.getLogger("udaconnect-srv")

# Dictionary to temporarily store locations
locations = {}

def get_app():
    from app import app
    return app

  
# Check if Kafka is ready by trying to connect to the broker
def is_kafka_ready():
    try:
        # Try connecting to Kafka broker without specifying a topic
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_SERVER,  # Kafka broker address in Docker
            group_id=KAFKA_CONSUMER_GROUP,
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

# Send location data to Kafka
def send_location_to_kafka(location_data):
    producer = create_producer()
    try:
        producer.send(KAFKA_TOPIC, location_data)
        producer.flush()  # Ensure the message is sent before returning
        logging.debug(f"Kafka message produced: {location_data}")
    except BaseException as e:
        logging.error(f"Error producing message: {e}")
   
def check_or_create_topic():
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_SERVER,
            client_id='location_service_admin'
        )

        # Get existing topics as a set
        existing_topics = set(admin_client.list_topics())
        if KAFKA_TOPIC not in existing_topics:
            logging.debug(f"Creating topic '{KAFKA_TOPIC}' on {KAFKA_SERVER}")
            topic = NewTopic(name=KAFKA_TOPIC, num_partitions=1, replication_factor=1)
            try:
                admin_client.create_topics(new_topics=[topic])
                logging.debug(f"Topic '{KAFKA_TOPIC}' created successfully.")
            except KafkaError as e:
                logging.error(f"Error creating topic '{KAFKA_TOPIC}': {e}")
                return False
        else:
            logging.debug(f"Topic '{KAFKA_TOPIC}' already exists on {KAFKA_SERVER}")
        
        logging.debug("Kafka Producer connection successful.")
        return True
    except NoBrokersAvailable:
        logging.warning("Kafka is not available yet. Retrying...")
        return False
    except KafkaError as e:
        logging.error(f"Kafka error occurred: {e}. Retrying...")
        return False