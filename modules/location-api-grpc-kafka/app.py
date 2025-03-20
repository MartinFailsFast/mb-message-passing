import grpc
from concurrent import futures
import time
import location_pb2
import location_pb2_grpc
from kafka_handler import send_location_to_kafka,consume_location_from_kafka,check_or_create_topic, locations, is_kafka_ready
import json
import logging

# Create a dictionary to store locations
#locations = {}
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-srv")

class LocationService(location_pb2_grpc.LocationServiceServicer):



    def CreateLocation(self, request, context):

        # Store the location in the dictionary
        locations[request.id] = request
        # Convert the location to JSON or string and send it to Kafka
        
        location_data = {
            'id': request.id,
            'latitude': request.latitude,
            'longitude': request.longitude,
            'creation_time': request.creation_time
        }

        logging.debug(f"Location data created: {location_data}")


        send_location_to_kafka(location_data)
        
        return request


    def test_producer():
        location_data = {
            'id': 1,
            'latitude': 1.0,
            'longitude': 1.0,
             'creation_time': "2025-03-17T14:30:00Z"
        }
        print(location_data)
        send_location_to_kafka(location_data)

        


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

    def GetAllLocations(self, request, context):
            # Retrieve all locations (returning them as a list)
            all_locations = list(locations.values())
            return location_pb2.GetAllLocationsResponse(locations=[location_pb2.Location(
                id=loc['id'], latitude=loc['latitude'], longitude=loc['longitude'], name=loc['name']) for loc in all_locations])




def serve():


    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
    
    
    # Health check endpoint
    server.add_insecure_port('[::]:5005')
    server.start()
    logging.debug("Server is running on port 5005...")
 

    
    # Wait for Kafka to be ready
    while not is_kafka_ready():
        logging.debug("Wait for Kafka to be ready...")
        time.sleep(10)  # Wait for 5 seconds before retrying
    
    # Ensure the topic exists
    #check_or_create_topic()
    LocationService.test_producer()

    # Consume messages from Kafka in a separate thread
    import threading
    #kafka_thread = threading.Thread(target=consume_location_from_kafka)
    #kafka_thread.start()

    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
