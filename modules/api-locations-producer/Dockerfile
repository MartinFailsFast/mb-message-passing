FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libc-dev libpq-dev build-essential python3-dev libffi-dev bash g++ cmake make libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Expose both Flask and gRPC ports
EXPOSE 5002
EXPOSE 5005

COPY . .


CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]
