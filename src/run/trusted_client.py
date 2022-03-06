"""
Trusted client is a sample client that uses for demo and testing
"""

import asyncio
import json
import time

from rpcudp_protocol import RPCProtocol

start_time = time.time()

class ClientProtocol(RPCProtocol):
    """
    class to call local methods
    """
    def __init__(self, wait_timeout=5, protocol=None):
        RPCProtocol.__init__(self, wait_timeout=wait_timeout)
        self.protocol=protocol

    def save_protocol_and_transport(self, protocol, transport):
        """
        Save the protocol and transport
        """
        self.protocol = protocol
        self.transport = transport

    def rpc_broadcast_complete(self, address, response):
        """
        call back used when broadcast complete.
        """
        print(f"\nBroadcast complete at: address: {address} {time.time() - start_time},"
              f" response: {response}")

protocol_class = ClientProtocol(5)

def _create_protocol():
    return protocol_class

loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(_create_protocol, local_addr=('127.0.0.1', 5090))
transport_returned, protocol_returned = loop.run_until_complete(listen)
protocol_class.save_protocol_and_transport(protocol=protocol_returned,
                                                transport=transport_returned)

sample_request = {
    "message": {
        "action": "nominate_node",
        "host": "127.0.0.1",
        "port": "5090"
    }
}

async def broadcast_message(protocol_to_use, address, request_to_use):
    """
    broadcast message to all nodes
    """
    result = await protocol_to_use.initiate_broadcast(address, json.dumps(request_to_use))
    print(result[1] if result[0] else "No response received.")
    print(f"\ntime_elapsed: {time.time() - start_time}")
    #start_time2 = time.time()
    #result2 = await protocol_to_use.validate_broadcast(address, json.dumps(request_to_use))
    #print(result2[1] if result2[0] else "No response received.")
    #print(f"\ntime_elapsed2: {time.time() - start_time2}")

loop.run_until_complete(broadcast_message(protocol_returned, ('127.0.0.1', 6100), sample_request))
loop.run_forever()
