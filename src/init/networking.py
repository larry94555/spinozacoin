import command
from request import Request
from request_handler import RequestHandler
from typing import Final
import util

class Networking:

    def __init__(self, node):
        self.node = node
        self.SPINOZA_COIN_PREFIX: Final = b'\x02\x03\x05\x07'
        self.SPINOZA_COIN_SUFFIX: Final = b'\x07\x07\x07\x07'
        self.PREFIX_SIZE: Final = len(self.SPINOZA_COIN_PREFIX)
        self.SUFFIX_SIZE: Final = len(self.SPINOZA_COIN_SUFFIX)

    async def announce_to(self, destination_host, destination_port):
        request = Request(
            networking=self,
            identifier = self.node.get_public_key_value(),
            json = { 
                "action": command.ANNOUNCE_NODE,
                "host": self.node.host,
                "port": self.node.port
            }
        )
        return await request.send_to(destination_host, destination_port)

    def get_identifier(self):
        return 123

    def get_response(self, request_json):

        command_handler = {
            command.ANNOUNCE_NODE: self.handle_announce_node,
            command.UPTAKE_CHECKPOINT: self.handle_uptake_checkpoint,
            command.NODE_DOWN: self.handle_node_down,
            command.NODE_UNRELIABLE: self.handle_node_unreliable,
            command.READY_TO_JOIN: self.handle_ready_to_join,
            command.NOMINATE_CHECKPOINT: self.handle_nominate_checkpoint,
            command.VALIDATE_CHECKPOINT: self.handle_validate_checkpoint
        }

        # need to change, json/json seems wrong....
        action = request_json['json']['json']['action']
        return command_handler[action](request_json)

    def handle_announce_node(self, request_json):
        return {
            "checkpoint": 0,
            "node": "nodeinfo"
        }
            
    def handle_uptake_checkpoint(self, request_json):
        pass

    def handle_node_down(self, request_json):
        pass

    def handle_node_unreliable(self, request_json):
        pass

    def handle_ready_to_join(self, request_json):
        pass

    def handle_nominate_checkpoint(self, request_json):
        pass

    def handle_validate_checkpoint(self, request_json):
        pass

    async def listen(self):
        request_handler = RequestHandler(self)
        return await request_handler.run() 
