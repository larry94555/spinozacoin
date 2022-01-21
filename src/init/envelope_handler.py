import asyncio
from envelope import Envelope
import json

class EnvelopeHandler:

    def __init__(self, networking):
        self.networking = networking

    async def handle_connection(self, reader, writer):
        # wait for message - nned to constrain by size
        data_received = await reader.readuntil(self.networking.SPINOZA_COIN_SUFFIX)
        print(f"Received: {data_received}")
        try:
            if not data_received.startswith(self.networking.SPINOZA_COIN_PREFIX):
                print("Bad prefix... closing")
            if not data_received.endswith(self.networking.SPINOZA_COIN_SUFFIX):
                print("Bad suffix... closing")
           
            action = data_received[self.networking.PREFIX_SIZE:-self.networking.SUFFIX_SIZE].decode()
            dictionary = json.loads(action)
            print(f"Action received: {dictionary['json']['action']}")
            
        except Exception as e:
            print(f"hit issue parsing action with error: {e}")
        await writer.write("sending response...\n".encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def run(self):
        return await asyncio.start_server(
	    self.handle_connection, 
            self.networking.node.host, 
            self.networking.node.port,
            limit = 10000
        )
