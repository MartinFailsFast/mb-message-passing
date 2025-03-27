import os

class Config:
    # Kafka configuration
    KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka:9092')  # Default to localhost:9092
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'location-topic')  # Default topic name
    KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'location-consumer-group')  # Default group

    DB_USERNAME = os.environ["DB_USERNAME"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]


    # PostgreSQL configuration
    DB_URI = os.getenv('DB_URI', 'postgresql://postgres:password@localhost:5432/mydb')  # Default DB URI
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"   
    )

    # Retry settings
    RETRY_INTERVAL = int(os.getenv('RETRY_INTERVAL', 5))  # Retry interval in seconds, default 5 seconds
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 10))  # Maximum retries 