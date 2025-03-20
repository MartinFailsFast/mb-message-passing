import os
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic


app = Flask(__name__)

# Get Kafka server from environment (set by Docker Compose)
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC_NAME = 'location-topic'

# Dictionary to temporarily store locations
locations = {}

def create_producer():
    # Setup Kafka producer with kafka-python
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    create_topic_if_not_exists()

    return producer


# Create Kafka consumer
def create_consumer():
    conf = {
        'bootstrap.servers': KAFKA_SERVER,
        'group.id': 'location-consumer-group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([TOPIC_NAME])
    return consumer


def send_location_to_kafka(location_data):
    producer = create_producer()
    try:
        producer.produce(TOPIC_NAME, location_data.encode('utf-8'))
        producer.flush()  # Ensure the message is sent before returning
    except KafkaException as e:
        print(f"Error producing message: {e}")

# Function to consume a message from Kafka and store the location in the dictionary
def consume_location_from_kafka():
    consumer = create_consumer()
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for new messages
            if msg is None:
                continue  # No message available
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached {0}'.format(msg))
                else:
                    print(msg.error())
            else:
                location_data = msg.value().decode('utf-8')
                location = json.loads(location_data)
                # Store location in the dictionary with ID as the key
                locations[location['id']] = location
    finally:
        consumer.close()

# Create Kafka AdminClient to check or create topics
def create_admin_client():
    conf = {
        'bootstrap.servers': KAFKA_SERVER,
    }
    admin_client = AdminClient(conf)
    return admin_client

def check_or_create_topic():
    admin_client = create_admin_client()

    # List existing topics
    try:
        topics = admin_client.list_topics(timeout=10).topics
        if TOPIC_NAME in topics:
            print(f"Topic '{TOPIC_NAME}' already exists.")
        else:
            print(f"Topic '{TOPIC_NAME}' does not exist. Creating it...")
            # Create the topic if it doesn't exist
            # You can configure the topic creation (partitions, replication_factor) as needed
            futures = admin_client.create_topics(
                [NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)]
            )
            for _, future in futures.items():
                try:
                    future.result()  # The result of the future should be None on success
                    print(f"Topic '{TOPIC_NAME}' created successfully.")
                except KafkaException as e:
                    print(f"Failed to create topic: {e}")
    except KafkaException as e:
        print(f"Error while listing topics: {e}")


