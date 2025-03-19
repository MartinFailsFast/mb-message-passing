FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV DB_USERNAME="ct_admin"
ENV DB_PASSWORD="hotdogsfordinner"
ENV DB_NAME="geoconnections"
ENV DB_HOST="host.docker.internal"
ENV DB_PORT="5432"

EXPOSE 5001

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0","--port", "5001"]