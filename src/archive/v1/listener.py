import asyncio
from challenge_result import ChallengeResult
from request import Request
from response import Response
import json

class Listener:

    def __init__(self, networking):
        self.networking = networking

    async def handle_connection(self, reader, writer):
        # wait for message - nned to constrain by size
        try:
            client_w = writer.get_extra_info('peername')
        except Exception as e:
            print(f"Listener: handle_connection: error with: {e}")
        data_received = await reader.readuntil(self.networking.SPINOZA_COIN_SUFFIX)
        print(f"\nListener: instance {self.networking.node.instance_id}: handle_connection: Received: {data_received}")
        try:
            if not data_received.startswith(self.networking.SPINOZA_COIN_PREFIX):
                print("Bad prefix... closing")
            if not data_received.endswith(self.networking.SPINOZA_COIN_SUFFIX):
                print("Bad suffix... closing")
           
            request_encoded = data_received[self.networking.PREFIX_SIZE:-self.networking.SUFFIX_SIZE].decode()
            request_json = json.loads(request_encoded)
            
            response_json = self.networking.handle_request.get_response(request_json)
            response = Response(
                reader = reader,
                writer = writer,
                networking = self.networking,
                identifier = self.networking.get_identifier(), 
                payload_json = response_json
            )
            response.respond()
            challenge_answer_received = await reader.readuntil(self.networking.SPINOZA_COIN_SUFFIX)
            print(f"\nListener: handle_connection: instance {self.networking.node.instance_id} challenge_answer_received: handle_connection: Received: {challenge_answer_received}")
            # validate answer to challenge
            answer_encoded = challenge_answer_received[self.networking.PREFIX_SIZE:-self.networking.SUFFIX_SIZE].decode()
            answer_json = json.loads(answer_encoded)
            challenge_result = ChallengeResult(
                reader = reader,
                writer = writer,
                networking = self.networking,
                identifier = self.networking.get_identifier(),
                payload_json = self.networking.handle_challenge.get_result(answer_json)
            )
            challenge_result.send()
            
            
        except Exception as e:
            print(f"Listener: handle_connection: hit issue parsing action with error: {e}")
        print("Closing...")
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
