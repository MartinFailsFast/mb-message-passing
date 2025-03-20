# Use the official Python image as a base
FROM python:3.13
#FROM python:3.7-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc libc-dev libpq-dev build-essential python3-dev libffi-dev bash g++ cmake make
    
# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your application runs on (if applicable)
EXPOSE 5005
# Command to run your application
#CMD ["python3", ".\app.py"]  # Change this to your main application file
CMD ["python3", "app.py"] 