import os
import logging


from app import create_app

# Configure global logging
'''
logging.basicConfig(
    level=logging.DEBUG,  # or use logging.INFO, depending on your needs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # This ensures logs are printed to stdout
)
'''

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
     app.run(debug=True)
