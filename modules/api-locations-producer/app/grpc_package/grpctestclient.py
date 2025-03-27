import grpc
from . import location_pb2, location_pb2_grpc

def run():
    print("Sending sample payload...")
    # Create a channel to the gRPC server
    channel = grpc.insecure_channel('localhost:5005')
    


    # Create a stub (client)
    stub = location_pb2_grpc.LocationServiceStub(channel)
    
    my_message = location_pb2.Location(
        id=123,  # Use appropriate values for your fields
        person_id=456,
        longitude="123.456",
        latitude="78.910",
        creation_time="2025-03-20T00:00:00Z"
    )

    # Send the message and receive a response
    #response = stub.Location(my_message)
    response = stub.CreateLocation(my_message)
    
    print("Response from server:", response)

if __name__ == '__main__':
    run()

