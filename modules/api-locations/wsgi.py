import os
import sys
#print("PYTHON PATH:", sys.path)
import logging
import threading

# Debugging output to check PYTHONPATH
#print("PYTHON PATH:", sys.path)

# Manually add the grpc_package directory to sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'grpc_package')))
#print("PYTHON PATH:", sys.path)

# Check if grpc_package is accessible
#print("Does grpc_package exist?", os.path.isdir('/app/grpc_package'))

# Now try to import grpc_package
print(sys.path)
from app.grpc_package import appgrpc
#from app.grpc_package import location_pb2, location_pb2_grpc
# Test whether the import works
#print(location_pb2)
#print(location_pb2_grpc)

from app import create_app

# Start gRPC server in a separate thread
def start_grpc_server():
    appgrpc.serve()


# Start gRPC server in a separate thread
grpc_thread = threading.Thread(target=start_grpc_server) 
grpc_thread.daemon = True
grpc_thread.start()



app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
     app.run(debug=True)
