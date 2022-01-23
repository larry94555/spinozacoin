import asyncio
import command
from typing import Final
import json
from message import Message
import util

# the envelope has two parts:
# outer envelope:  Hash, Checksum, Pow
# inner envelope:  Signed by PrivateKey, Timestamp, OrderId
# command
# the goal is to wrap a command in the envelope which signifies:
# * the source of the message received
# * pow that shows that source understands the protocol
# * maximum size allowed, if size greater than max bytes, then close the connection
#
# Envelope is always for source when being built and always for the destination when being parsed

SEQUENCE_ID_FILE: Final = "sequence_id.txt"

class RequestClientProtocol(asyncio.Protocol):
    def __init__(self, envelope, loop):
        self.envelope = envelope
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print(f"RequestClientProtocol Data sent: {self.message}")

    def data_received(self, data):
        print(f"RequestClientProtocol Data received: {data}")

    def connection_lost(self, exc):
        print('RequestClientProtocol The server closed the connection')
        print('Stop the event loop')
        #self.loop.stop()

class Request:
 
    # synchronize on a file for now 
    def __init__(self, networking, identifier, action_json):
        self.networking = networking
        sequence_id = self.next_id()
        timestamp = util.utc_timestamp()
        request_body = {
                   "sequence_id": sequence_id,
                   "timestamp": timestamp,
                   "action": action_json
        }
        self.message = Message(networking, identifier, request_body)

    def next_id(self):
        return util.increase_and_return_value(self.networking.node.get_instance_path(), SEQUENCE_ID_FILE)

    async def send_to(self, destination_host, destination_port):
        # build
        try:
            transport, protocol = await self.networking.node.loop.create_connection(lambda: RequestClientProtocol(self, self.networking.node.loop), host=destination_host, port = destination_port)
            # This should be a command such as #send_node_info
            transport.write(self.message.get_encoded_payload())
            # There should always be a return envelope
            
        except Exception as e:
            print(f"Connection to {destination_host}:{destination_port} failed with error: {e}")
    
