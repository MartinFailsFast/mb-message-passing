import logging
import sys
from db.db_setup import init_db
from kafka_db.kafkaConsumer import start_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

def main():
    try:
        logger.info("Initializing database...")
        init_db()

        logger.info("Starting Kafka consumer...")
        start_consumer()  # Assuming this function blocks indefinitely to consume messages
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        sys.exit(1)  # Exit with non-zero status if an error happens

if __name__ == "__main__":
    main()