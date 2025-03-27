FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libc-dev libpq-dev build-essential python3-dev libffi-dev bash g++ cmake make libgeos-dev \
    && rm -rf /var/lib/apt/lists/*
    

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV DB_USERNAME="ct_admin"
ENV DB_PASSWORD="hotdogsfordinner"
ENV DB_NAME="geoconnections"
ENV DB_HOST="host.docker.internal"
ENV DB_PORT="5432"
ENV KAFKA_SERVER="kafka:9092"

COPY . /app

# Set the default command to run when the container starts
CMD ["python", "app.py"]