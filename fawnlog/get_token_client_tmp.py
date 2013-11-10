"""
   This is an example showing how to write client side rpc code
   using GetToken as an example.
   Please delete me.
"""

import config
import get_token_pb2
from protobuf.socketrpc import RpcService

# Create a request
request = get_token_pb2.GetTokenRequest()
request.number = 3

# Create a new service instance
service = RpcService(get_token_pb2.GetTokenService_Stub,
                     config.SEQUENCER_PORT,
                     config.SEQUENCER_HOST)

def callback(request, response):
    """Used for aync call."""
    print response.token

# Make a synchronous call
try:
    print "Make a synchronous call"
    response = service.GetToken(request, timeout=10000)
    print response.token
except Exception, ex:
    print ex

# Make an asynchronous call
try:
    print "Make an asynchronous call"
    response = service.GetToken(request, callback=callback)
except Exception, ex:
    print ex
