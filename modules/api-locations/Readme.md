SQL check: PGadmin
select * from location where person_id=5 and creation_time >='2019-07-05 15:00:00' and creation_time <='2025-07-07 15:00:00'

## Generating gRPC files
`pip install grpcio-tools`
`python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto`

## VAGRANT
vagrant status
C:\Users\Coding4Kids\udacity-training\cd0309-message-passing-projects-starter>
vagrant ssh
sudo su
kubectl get svc
kubectl port-forward postgres  --address 0.0.0.0 5432:5432



# Testing
kubectl port-forward svc/postgres 5432:5432
docker run -p 5002:5002 test
docker run -p 5002:5002 -p 5005:5005 test
 docker build -t test . --no-cache
 # Docker aufräumen
 docker system prune -af



POST REquest SAmple
DEBUG:root:Received data: {'person_id': 10, 'longitude': '53.12864919788544', 'latitude': '8.166434884071895', 'creation_time': '2025-03-07T18:00:00'}
DEBUG:udaconnect-srv:Received Kafka message: {'id': 6, 'latitude': '-118.2437', 'longitude': '34.0522', 'creation_time': '2023-10-01T14:30:00Z'}
 {'id': 1, 'latitude': 1.0, 'longitude': 1.0, 'creation_time': '2025-03-17T14:30:00Z'}

docker exec -it affectionate_johnson /bin/sh
apk add --no-cache curl
curl http://mb-cd0309-message-passing-projects-starter-api-persons-1:5001/api/locations?person_id=5&start_date=2020-01-01T00:00:00&end_date=2020-12-30T00:00:00

docker cp <container_name_or_id>:<path_in_container> <path_on_host>

docker cp affectionate_johnson:./app/app/grpc_package/location_pb2.py ./modules/api-locations/app/grpc_package
docker cp affectionate_johnson:./app/app/grpc_package/location_pb2_grpc.py ./modules/api-locations/app/grpc_package


# create proto:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. location.proto
python -m grpc_tools.protoc \
    -I. \
    --python_out=./grpc_package \
    --grpc_python_out=./grpc_package \
    grpc_package/location.proto

# Run -Test Client:
python -m app.grpc_package.grpchost

# Docker Compose
docker-compose build




# Virtuell ENV
python -m venv myvenv
.\myvenv\Scripts\activate
pip install -r requirements.txt
deactivate




# Requirements POD:
aniso8601              7.0.0
attrs                  19.1.0
certifi                2025.1.31
charset-normalizer     3.4.1
Click                  7.0
Flask                  1.1.1
flask-accepts          0.10.0
Flask-Cors             3.0.8
Flask-RESTful          0.3.7
flask-restplus         0.13.0
flask-restx            0.2.0
Flask-Script           2.0.6
Flask-SQLAlchemy       2.4.0
GeoAlchemy2            0.8.4
grpcio                 1.34.0
grpcio-tools           1.34.0
idna                   3.10
itsdangerous           1.1.0
Jinja2                 2.11.2
jsonschema             3.0.2
kafka-python           2.0.6
MarkupSafe             1.1.1
marshmallow            3.7.1
marshmallow-sqlalchemy 0.23.1
pip                    24.0
protobuf               3.14.0
psycopg2-binary        2.8.5
pyrsistent             0.16.0
python-dateutil        2.8.1
pytz                   2020.1
requests               2.31.0
setuptools             57.5.0
Shapely                1.7.0
six                    1.15.0
SQLAlchemy             1.3.19
urllib3                2.0.7
Werkzeug               0.16.1
wheel                  0.41.2



REST:
api-person-1     | DEBUG:root:Location: {'creation_time': '2020-08-15T10:37:06', 'latitude': '-122.290883', 'id': 30, 'person_id': 5, 'longitude': '37.55363'}


import requests

# Client class to fetch locations
class LocationClient:
    BASE_URL = "http://mb-cd0309-message-passing-projects-starter-api-locations-1:5001/api/locations"
    #http://{{host}}:{{port}}/api/persons

    def get_locations(self, person_id, start_date, end_date):
        """Fetch locations by person_id and time range."""
        params = {
            "person_id": person_id,
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            # Send the GET request
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an error for non-2xx responses

            # Return raw JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
        except Exception as e:
            print(f"Error handling response: {e}")
            return []

# Example usage
if __name__ == "__main__":
    client = LocationClient()
    print("Fetching locations...")
    person_id = 5
    start_date = "2020-07-07T18:00:00"
    end_date = "2025-07-07T18:00:00"

    locations = client.get_locations(person_id, start_date, end_date)

    if locations:
        print("Retrieved locations:")
        for loc in locations:
            print(
                f"ID: {loc.get('id')}, Person ID: {loc.get('person_id')}, Lat: {loc.get('latitude')}, Long: {loc.get('longitude')}, Time: {loc.get('creation_time')}"
            )
    else:
        print("No locations found.")
