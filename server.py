import grpc
from concurrent import futures
import numstore_pb2_grpc
import numstore_pb2
import threading
lock = threading.Lock()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[("grpc.so_reuseport", 0)])

lookUp = {}
total = 0
cache = {} # Using a LRU cache. For caching, I chose to cache the factorial values rather than the keys
cache_size = 10
evict_order = []
class Comp(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, request, context):
        global lookUp, total
        key = request.key
        val = request.value
        with lock:
            if key in lookUp:
                total -= lookUp[key]
            lookUp[key] = val
            total += val
        return numstore_pb2.SetNumResponse(total=total)
    
    def Fact(self, request, context):
        global lookUp
        key = request.key
        if key not in lookUp:
            return numstore_pb2.FactResponse(error="key not yet established")
        
        val = lookUp[key]
        if val in cache:
            with lock:
                evict_order.remove(val)
                evict_order.append(val)
            result = cache[val]
            return numstore_pb2.FactResponse(value=result, hit=True)
        
        result = self.factorial(val)
        with lock:
            cache[val] = result
            evict_order.append(val)
            if len(evict_order) > cache_size:
                removed = evict_order.pop(0)
                cache.pop(removed)
        return numstore_pb2.FactResponse(value=result, hit=False)
        
    def factorial(self, val):
        if val == 1 or val == 0:
            return 1
        return val * self.factorial(val-1)

numstore_pb2_grpc.add_NumStoreServicer_to_server(Comp(), server)
print("server running")
    
server.add_insecure_port('[::]:5440')
server.start()
server.wait_for_termination()
