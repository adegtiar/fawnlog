"""
   This is an example of the client side code using flash service.
   Please delete me.
"""

import config
import flash_service_pb2
from protobuf.socketrpc import RpcService


(host, port) = config.SERVER_ADDR_LIST[0]
# Create a new service instance
service = RpcService(flash_service_pb2.FlashServer_Stub,
                     host, port)

#  Read
request_r = flash_service_pb2.ReadRequest()
request_r.offset = 10000

# Make a synchronous call
try:
    print "Call read"
    response_r = service.Read(request_r, timeout=10000)
    print response_r.status
    print response_r.data
except Exception, ex:
    print ex


# Write
request_w = flash_service_pb2.WriteRequest()
request_w.offset = 1123123
request_w.data = "datadatadatadatadatadata"
try:
    print "Call write"
    response_w = service.Write(request_w, timeout=10000)
    print response_w.status
except Exception, ex:
    print ex
