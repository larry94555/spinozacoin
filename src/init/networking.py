import command
from handle_request import HandleRequest
from handle_response import HandleResponse
from request import Request
from request_handler import RequestHandler
from typing import Final
import util

class Networking:

    def __init__(self, node):
        self.node = node
        self.handle_request = HandleRequest(self)
        self.handle_response = HandleResponse(self)
        self.SPINOZA_COIN_PREFIX: Final = b'\x02\x03\x05\x07'
        self.SPINOZA_COIN_SUFFIX: Final = b'\x07\x07\x07\x07'
        self.PREFIX_SIZE: Final = len(self.SPINOZA_COIN_PREFIX)
        self.SUFFIX_SIZE: Final = len(self.SPINOZA_COIN_SUFFIX)

    async def announce_to(self, destination_host, destination_port):
        request = Request(
            networking=self,
            identifier = self.node.get_public_key_value(),
            action_json = { 
                "action_type": command.ANNOUNCE_NODE,
                "host": self.node.host,
                "port": self.node.port
            }
        )
        return await request.send_to(destination_host, destination_port)

    async def check_hash_with(self, destination_host, destination_port, checkpoint, hash):
        print(f"check_hash_with: destination_host: {destination_host}, destination_port: {destination_port}, checkpoint: {checkpoint}, hash: {hash}")
        request = Request(
            networking=self,
            identifier = self.node.checkpoint if self.node.checkpoint != None else self.node.get_public_key_value(),
            action_json = {
                "action_type": command.CHECK_HASH,
                "checkpoint": checkpoint,
                "hash": hash
            }
        )
        return await request.send_to(destination_host, destination_port)

    def get_identifier(self):
        return self.node.checkpoint

    async def listen(self):
        print(f"\nlisten: port: {self.node.port}")
        request_handler = RequestHandler(self)
        return await request_handler.run() 
