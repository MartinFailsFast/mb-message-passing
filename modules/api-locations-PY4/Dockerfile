#FROM python:3.7-slim
FROM python:3.13
#FROM python:3.14-slim


WORKDIR /app

#RUN apt-get update && apt-get install -y \
 #   gcc libc-dev libpq-dev build-essential python3-dev libffi-dev bash g++ cmake make

RUN apt-get update && apt-get install -y \
 gcc libc-dev libpq-dev build-essential python3-dev libffi-dev bash g++ cmake make libgeos-dev

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Patch für flask_restplus -> flask_restx und MutableMapping Problem
#RUN sed -i 's/from collections import MutableMapping/from collections.abc import MutableMapping/' /usr/local/lib/python3.13/site-packages/flask_restplus/model.py
#RUN sed -i 's/from flask_restplus/model import Model/from flask_restx/model import Model/' /usr/local/lib/python3.13/site-packages/flask_accepts/decorators/decorators.py
#RUN sed -i 's/from flask_restplus/ from flask_restx/' /usr/local/lib/python3.13/site-packages/flask_accepts/decorators/decorators.py


ENV DB_USERNAME="ct_admin"
ENV DB_PASSWORD="hotdogsfordinner"
ENV DB_NAME="geoconnections"
ENV DB_HOST="host.docker.internal"
ENV DB_PORT="5432"
ENV PERSON_HOST="http://mb-cd0309-message-passing-projects-starter-api-person-1:5001/api/persons"
                        

EXPOSE 5002

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]
