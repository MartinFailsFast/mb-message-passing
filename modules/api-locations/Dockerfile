FROM python:3.11-slim
# 3.7 3.13
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libc-dev libpq-dev build-essential python3-dev libffi-dev bash g++ cmake make libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

    

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DB_USERNAME="ct_admin"
ENV DB_PASSWORD="hotdogsfordinner"
ENV DB_NAME="geoconnections"
ENV DB_HOST="host.docker.internal"
ENV DB_PORT="5432"
ENV PERSON_HOST="http://mb-cd0309-message-passing-projects-starter-api-person-1:5001/api/persons"
ENV PYTHONPATH="/app"

# Expose both Flask and gRPC ports
EXPOSE 5002
EXPOSE 5005

COPY . .


CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]
