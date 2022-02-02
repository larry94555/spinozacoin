from answer_to_challenge import AnswerToChallenge
import asyncio
from request import Request
from response import Response
import json

class Listener:

    def __init__(self, networking):
        self.networking = networking

    async def handle_connection(self, reader, writer):
        # wait for message - nned to constrain by size
        print(f"\nRequestHandler: handle_connection: ", flush=True)
        try:
            client_w = writer.get_extra_info('peername')
            print(f"\nclient_w: {client_w}")
        except Exception as e:
            print(f"Hit error with: {e}")
        data_received = await reader.readuntil(self.networking.SPINOZA_COIN_SUFFIX)
        print(f"\nRequestHandler: handle_connection: Received: {data_received}")
        try:
            if not data_received.startswith(self.networking.SPINOZA_COIN_PREFIX):
                print("Bad prefix... closing")
            if not data_received.endswith(self.networking.SPINOZA_COIN_SUFFIX):
                print("Bad suffix... closing")
           
            request_encoded = data_received[self.networking.PREFIX_SIZE:-self.networking.SUFFIX_SIZE].decode()
            request_json = json.loads(request_encoded)
            
            response_json = self.networking.handle_request.get_response(request_json)
            print(f"\nhandle_connection: response_json: {response_json}")
            response = Response(
                reader = reader,
                writer = writer,
                networking = self.networking,
                identifier = self.networking.get_identifier(), 
                payload_json = response_json
            )
            response.respond()
            challenge_received = await reader.readuntil(self.networking.SPINOZA_COIN_SUFFIX)
            print(f"\nRequestHandler (part 2): handle_connection: Received: {challenge_received}")
            # validate answer to challenge
            answerToChallenge = AnswerToChallenge(
                reader = reader,
                writer = writer,
                networking = self.networking,
                identifier = self.networking.get_identifier(),
                payload_json = response_json
            )
            answerToChallenge.evaluate()
            
        except Exception as e:
            print(f"hit issue parsing action with error: {e}")
        print("Closing...")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def run(self):
        print("\nhandle_request: run")
        return await asyncio.start_server(
	    self.handle_connection, 
            self.networking.node.host, 
            self.networking.node.port,
            limit = 10000
        )