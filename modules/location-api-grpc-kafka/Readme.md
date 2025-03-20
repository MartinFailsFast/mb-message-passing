

## Generating gRPC files
`pip install grpcio-tools`

`python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ order.proto`

# Generate Python Code from Protobuf
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. location.proto
ls
# Build and deploy a Docker file
docker build -t location-api .
docker run -p 5005:5005 location-api

# You can test the endpoint with this Python class
grpcClient.py


# Docker Compose:
  location-api-grpc-kafka:
    #image: mb-cd0309-message-passing-projects-starter-api-person
    build:
      context: ./location-api-grpc-kafka
    ports:
      - "5005:5005"
    depends_on:
      - kafka
    environment:
      <<: *env_vars
    networks:
      - udaconnect_network





#
path to dockerfile
/c/Users/Coding4Kids/udacity-training/mb-message-passing/modules/api-locations-PY4


syntax = "proto3";

package location;

// The Location message
message Location {
    int32 id = 1;
    int32 person_id = 2;
    string longitude = 3;
    string latitude = 4;
    string creation_time = 5;
}

// The service that handles location operations
service LocationService {
    // RPC to create a location
    rpc CreateLocation (Location) returns (Location);
    // RPC to get a location by ID
    rpc GetLocation (Location) returns (Location);
}


'



            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached {0}'.format(msg))
                else:
                    print(msg.error())
            else:
                location_data = 
                location = json.loads(location_data)
                # Store location in the dictionary with ID as the key
                locations[location['id']] = location