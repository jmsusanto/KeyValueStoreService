import sys
import grpc
import numstore_pb2, numstore_pb2_grpc
import numpy as np
import threading
import time

lock = threading.Lock()
# STATS
hits = 0
total = 0
port = sys.argv[1]
addr = f"127.0.0.1:{port}"
channel = grpc.insecure_channel(addr)
stub = numstore_pb2_grpc.NumStoreStub(channel)
keys = [str(i) for i in range(100)]
latencies = []

def send_random_requests():
    global hits, total
    local_hits = 0
    local_requests = 0
    requests = 100
    for req in range(requests):
        function = np.random.randint(0, 2)
        random_key = np.random.choice(keys)
        if function:
            start = time.time()
            resp = stub.Fact(numstore_pb2.FactRequest(key=random_key))
            latencies.append(time.time() - start)
            local_requests += 1
            if resp.hit:
                local_hits += 1
        else:
            start = time.time()
            random_value = np.random.randint(1, 16)
            resp = stub.SetNum(numstore_pb2.SetNumRequest(key=random_key, value=random_value))
            latencies.append(time.time() - start)
            
    with lock:
        total += local_requests
        hits += local_hits

threads = [None] * 8
for i in range(8):
    threads[i] = threading.Thread(target=send_random_requests)
    threads[i].start()
    
for i in range(8):
    threads[i].join()

# HIT RATE
print("hit rate at:", str(round(hits/total*100, 1)) + "%")

# P50 RESPONSE TIME
p50 = sum(latencies) / len(latencies) * 1000
print("p50 response time of:", round(p50, 3), "ms")

# P50 RESPONSE TIME
print("p99 response time of:", round(np.quantile(latencies, 0.99)*1000, 3), "ms")
