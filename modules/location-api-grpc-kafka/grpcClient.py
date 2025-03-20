import grpc
import location_pb2
import location_pb2_grpc

'''
Client to send and receive grpc test messages to server
'''

def run():
        # Create a channel to the gRPC server
    channel = grpc.insecure_channel('localhost:5005')  # Adjust the address and port as needed
    
    # Create a stub (client)
    stub = location_pb2_grpc.LocationServiceStub(channel)
    
         # Create a new location message
    new_location1 = location_pb2.Location(
        id=1,
        person_id=123,
        longitude="34.0522",
        latitude="-118.2437",
        creation_time="2025-03-17T14:30:00Z"
    )

    new_location2 = location_pb2.Location(
        id=2,
        person_id=123,
        longitude="40.0522",
        latitude="-120.2437",
        creation_time="2025-03-17T14:30:00Z"
    )

    create_location(stub, new_location1)
    create_location(stub, new_location2)

    get_location_by_id(stub, 1)

    # Get all locations
    get_all_locations(stub)





def create_location(stub, new_location):
     # Call the CreateLocation RPC
    try:
        created_location = stub.CreateLocation(new_location)
        print(f"Created Location: ID={created_location.id}, Person ID={created_location.person_id}, "
            f"Coordinates=({created_location.latitude}, {created_location.longitude}), Time={created_location.creation_time}")
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()} - {e.details()}")

    
def get_location_by_id(stub, locationId):
    # Call the GetLocation RPC
    retrieved_location = stub.GetLocation(location_pb2.Location(id=locationId))
    print(f"Retrieved Location: ID={retrieved_location.id}, Person ID={retrieved_location.person_id}, "
            f"Coordinates=({retrieved_location.latitude}, {retrieved_location.longitude}), Time={retrieved_location.creation_time}")


def get_all_locations(stub):
    request = location_pb2.GetAllLocationsRequest()
    response = stub.GetAllLocations(request)
    print("All Locations:")
    for location in response.locations:
        print(f"ID={location.id}, Person ID={location.person_id}, "
              f"Coordinates=({location.latitude}, {location.longitude}), Time={location.creation_time}")

if __name__ == '__main__':
    run()