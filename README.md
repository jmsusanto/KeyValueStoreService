# KeyValueStoreService
A simple K/V store server that records number values for different string keys. Similar to a Python dictionary, but via a service that could be shared by code running on different computers.

The entire project is deployed on a docker container for portability, consistency, and various other benefits.

## Requirements
pip3 install grpcio grpcio-tools    
install docker on your machine

## Usage
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. numstore.proto   
docker build -t keyvalue .    
docker run -d -p 54321:5440 keyvalue    
python3 client.py 54321 > out.txt   
cat out.txt   

## Description
### server.py   
The server has 2 key functions. SetNum takes a key (string) and value (int) as parameters and returns a total (int). Fact takes a key (string) as a parameter and does a lookup of the value from the global dictionary corresponding to that key, then return the factorial of that value.

### client.py
The client is a demonstration on how to use server.py. This particular script starts some threads or processes that send random requests to the server, with the following features:    
- 8 threads/processes
- each thread/process sends 100 random requests to the server
- for each request, randomly decide between SetNum and Fact (50/50 mix)
- for each request, randomly choose a key (from a list of 100 possible keys)
- for SetNum requests, randomly select a number between 1 and 15


