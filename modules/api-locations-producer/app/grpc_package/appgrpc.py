import grpc
from concurrent import futures
import time
#from grpc_package import location_pb2, location_pb2_grpc
from . import location_pb2, location_pb2_grpc
from app.kafka_Producer import send_location_to_kafka,locations, check_or_create_topic
import json
import logging
import threading

# Create a dictionary to store locations
#locations = {}
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('kafka').setLevel(logging.WARNING) 
logger = logging.getLogger("udaconnect-srv")

class LocationService(location_pb2_grpc.LocationServiceServicer):



    # Implement the CreateLocation RPC method
    def CreateLocation(self, request, context):
        location_data = request
        logging.debug(f"GRPC location data received: {request}")

        # Convert the location to JSON or string and send it to Kafka    
        location_data = {
            'person_id': request.person_id,
            'latitude': request.latitude,
            'longitude': request.longitude,
            'creation_time': request.creation_time
        }
        # Store the location in the dictionary
        locations[request.id] = location_data
        
        send_location_to_kafka(location_data)
        
        return request


        

    # Implement the GetLocation RPC method
    def GetLocation(self, request, context):
        # Retrieve the location by ID from the Kafka topic
        location = locations.get(request.id)
        if location:
            # Convert the dictionary back into a Location proto
            return location_pb2.Location(
                id=location['id'],
                latitude=location['latitude'],
                longitude=location['longitude'],
                name=location['name']
            )
        else:
            context.set_details('Location not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return location_pb2.Location()

    # Implement the GetAllLocations RPC method
    def GetAllLocations(self, request, context):
            # Retrieve all locations (returning them as a list)
            all_locations = list(locations.values())
            return location_pb2.GetAllLocationsResponse(locations=[location_pb2.Location(
                id=loc['id'], latitude=loc['latitude'], longitude=loc['longitude'], name=loc['name']) for loc in all_locations])


def serve():

    # Start the gRPC server
    logging.debug("Starting gRPC server on port 5005...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
    
    
    # Health check endpoint
    server.add_insecure_port('[::]:5005')
    server.start()
    logging.debug("gRPC server started on port 5005.")

    # Wait for Kafka to be ready
    while not check_or_create_topic():
        logging.debug("Wait for Kafka to be ready...")
        time.sleep(10)  

    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
