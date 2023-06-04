FROM ubuntu:22.10
RUN apt-get update
RUN apt-get install -y python3 python3-pip curl lsof
RUN pip3 install numpy grpcio grpcio-tools
COPY server.py .
COPY numstore_pb2.py .
COPY numstore_pb2_grpc.py . 
CMD ["python3", "-u", "server.py", "&>", "log.txt", "&"]

