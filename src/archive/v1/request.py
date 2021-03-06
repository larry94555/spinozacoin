import asyncio
import command
from typing import Final
import json
from message import Message
import util

REQUEST_SEQUENCE_ID_FILE: Final = "request_sequence_id.txt"

class RequestClientProtocol(asyncio.Protocol):
    def __init__(self, request, loop):
        self.request = request
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print(f"RequestClientProtocol Data sent: {self.message.encoded_payload}")

    def data_received(self, data_received):
        print(f"\nRequestClientProtocol instance {self.request.networking.node.instance_id} Data received: {data_received}")
        # convert to json
        try:
            if not data_received.startswith(self.request.networking.SPINOZA_COIN_PREFIX):
                print("Bad prefix... closing")
            if not data_received.endswith(self.request.networking.SPINOZA_COIN_SUFFIX):
                print("Bad suffix... closing")

            response_encoded = data_received[self.request.networking.PREFIX_SIZE:-self.request.networking.SUFFIX_SIZE].decode()
            response_json = json.loads(response_encoded)
            task=asyncio.create_task(self.request.networking.handle_response.run(response_json, self.request.transport))
 
        except Exception as e:
            print(f"hit issue parsing action with error: {e}") 
        

    def connection_lost(self, exc):
        print(f'\nRequestClientProtocol The server closed the connection: {exc}')
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
        return util.increase_and_return_value(self.networking.node.get_instance_path(), REQUEST_SEQUENCE_ID_FILE)

    async def send_to(self, destination_host, destination_port):
        try:
            print(f"\nrequest: instance {self.networking.node.instance_id} send_to: host: {destination_host}, port: {destination_port}, message: {self.message.get_encoded_payload()}")
            # Create connection per request
            transport, protocol = await self.networking.node.loop.create_connection(lambda: RequestClientProtocol(self, self.networking.node.loop), host=destination_host, port = destination_port)
            # This should be a command such as #send_node_info
            transport.write(self.message.get_encoded_payload())
            self.transport = transport
            
        except Exception as e:
            print(f"request: send_to: Connection to {destination_host}:{destination_port} failed with error: {e}")

