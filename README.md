# KeyValueStoreService
A simple K/V store server that records number values for different string keys. Similar to a Python dictionary, but via a service that could be shared by code running on different computers.

The entire project is deployed on a docker container for portability, consistency, and various other benefits.

## Requirements
pip3 install grpcio grpcio-tools

## Usage
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. numstore.proto
python3 server.py &
python3 client.py 5440
