import os
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, NoBrokersAvailable
import json
import logging
import time
from app.udaconnect.services import ConnectionService, LocationService


# Get Kafka server from environment (set by Docker Compose)
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC_NAME = 'location-topic'

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('kafka').setLevel(logging.WARNING)
logger = logging.getLogger("udaconnect-srv")

# Dictionary to temporarily store locations
locations = {}


def is_kafka_readyold():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_SERVER,
            group_id='location-consumer-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        consumer.close()
        logging.debug("Kafka connection successful.")
        return True
    except NoBrokersAvailable:
        logging.debug("Kafka is not available yet. Retrying...")
        return False
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


def create_producer():
    check_or_create_topic()
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages as JSON
    )




def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_SERVER,
        group_id='location-consumer-group',
        auto_offset_reset='earliest',  # Read from the beginning if no offset
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize JSON value
    )

def send_location_to_kafka(location_data):
    producer = create_producer()
    try:
        producer.send(TOPIC_NAME, location_data)
        producer.flush()  # Ensure the message is sent before returning
        logging.debug(f"Produced message: {location_data}")
    except BaseException as e:
        logging.error(f"Error producing message: {e}")

# Function to consume a message from Kafka and store the location in the dictionary
def consume_location_from_kafkaold():
    consumer = create_consumer()
    try:
        while True:
            msg = consumer.poll(timeout_ms=1000)  # Poll for new messages
            if msg is None:
                continue  # No message available
            if msg is not None:
                location_data = msg.value().decode('utf-8')
                location = json.loads(location_data)
                locations[location['id']] = location
                print(f"Consumed location: {location}")
    finally:
        consumer.close()



# Simulate creating a new location from the Kafka message
def process_message(location_data):
    try:
        # Simulate creating a new Location in the database
        location = LocationService.create(location_data)
        logger.info(f"Created location: {location}")
        return location
    except Exception as e:
        logger.error(f"Error creating location: {e}")
        return None

# Function to consume a message from Kafka and store the location in the dictionary
def consume_location_from_kafkaOLD():
    consumer = create_consumer()  # Create a consumer
    try:
        while True:
            # Poll for messages, timeout after 1 second
            msg = consumer.poll(timeout_ms=1000)  
            if msg is None:
                continue  # No message available, keep polling
            for _, messages in msg.items():
                for message in messages:
                    location = message.value  # Deserialize message
                    # Store the location in the locations dictionary
                    locations[location['id']] = location
                    print(f"Consumed location: {location}")
    finally:
        consumer.close()  # Close the consumer when done


def consume_location_from_kafkatmp():
    consumer = create_consumer() 
    # Start consuming messages from Kafka
    for message in consumer:
        try:
            message_value = message.value
            # Assuming message is already decoded and is a dict.
            if isinstance(message, bytes):
                message_value = json.loads(message.decode('utf-8'))  # Only decode if it's in bytes
            
            
            logger.debug(f"Received Kafka message: {message_value}")

            # Assuming the schema is validated and processed in LocationService.create
            location = process_message(message_value)
            
            if location:
                logger.info(f"Successfully processed message and created location: {location}")
            else:
                logger.error(f"Failed to process message: {location_data}")
        
        except Exception as e:
            logger.error(f"Error processing Kafka message: {e}")

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



# Create Kafka AdminClient to check or create topics
def check_or_create_topic():
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
            logging.debug(f"Topic '{TOPIC_NAME}' created successfully.")
        else:
            logging.debug(f"Topic '{TOPIC_NAME}' already exists.")
    
    except NoBrokersAvailable:
        logging.debug("Warning: Kafka broker not available. Continuing without Kafka.")
    
    except KafkaError as e:
        logging.debug(f"Warning: Kafka error occurred: {e}. Continuing without Kafka.")