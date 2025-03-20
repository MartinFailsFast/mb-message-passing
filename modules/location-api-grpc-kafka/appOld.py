import grpc
from concurrent import futures
import time
import location_pb2
import location_pb2_grpc

# Create a dictionary to store locations
locations = {}

class LocationService(location_pb2_grpc.LocationServiceServicer):

    
    def CreateLocation(self, request, context):
        # Store the location in the dictionary
        locations[request.id] = request
        return request

    def GetLocation(self, request, context):
        # Retrieve the location by ID
        if request.id in locations:
            return locations[request.id]
        else:
            context.set_details('Location not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return location_pb2.Location()

    def GetAllLocations(self, request, context):
        # Retrieve all locations (returning them as a list)
        all_locations = list(locations.values())
        return location_pb2.GetAllLocationsResponse(locations=all_locations)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
    
    # Health check endpoint
    server.add_insecure_port('[::]:5005')
    server.start()
    print("Server is running on port 5005...")
    
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
