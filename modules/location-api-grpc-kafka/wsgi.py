import grpc
from concurrent import futures
import location_pb2_grpc  # Assuming you have generated gRPC files from .proto
from app.udaconnect.services import LocationService  # Your gRPC service implementations


# gRPC server setup
class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    # Implement your gRPC service methods here
    def CreateLocation(self, request, context):
        # Implement location creation logic
        pass
    
    def GetLocation(self, request, context):
        # Implement location retrieval logic
        pass
    
    def GetAllLocations(self, request, context):
        # Implement all locations retrieval logic
        pass

before_request
def before_request():
    # Set up a Kafka producer
    TOPIC_NAME = 'items'
    KAFKA_SERVER = 'localhost:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    # Setting Kafka to g enables us to use this
    # in other parts of our application
    g.kafka_producer = producer


def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
    server.add_insecure_port('[::]:50051')  # gRPC server on port 50051
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

def create_grpc_app():
    # Start the gRPC server in the background (use threading if you need)
    run_grpc_server()

if __name__ == "__main__":
    create_grpc_app()


import json

from kafka import KafkaProducer
from flask import Flask, jsonify, request, g, Response

from .services import retrieve_orders, create_order

app = Flask(__name__)


@app.before_request
def before_request():
    # Set up a Kafka producer
    TOPIC_NAME = 'items'
    KAFKA_SERVER = 'localhost:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    # Setting Kafka to g enables us to use this
    # in other parts of our application
    g.kafka_producer = producer


@app.route('/health')
def health():
    return jsonify({'response': 'Hello World!'})


@app.route('/api/orders/computers', methods=['GET', 'POST'])
def computers():
    if request.method == 'GET':
        return jsonify(retrieve_orders())
    elif request.method == 'POST':
        request_body = request.json
        result = create_order(request_body)
        #send2Kafka(request_body)
        #return jsonify(result)
        return Response(status=202)
    else:
        raise Exception('Unsupported HTTP request type.')





def send2Kafka(request_body):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    print(f"Sending message to '{TOPIC_NAME}'")
    producer.send(TOPIC_NAME, b'{request_body}')
    producer.flush()

if __name__ == '__main__':
    app.run()
