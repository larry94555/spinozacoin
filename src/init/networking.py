import command
from handle_challenge import HandleChallenge
from handle_request import HandleRequest
from handle_response import HandleResponse
from listener import Listener
from request import Request
import util

class Networking:

    def __init__(self, node):
        self.node = node
        self.handle_request = HandleRequest(self)
        self.handle_response = HandleResponse(self)
        self.handle_challenge = HandleChallenge(self)
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

    async def ready_to_join(self, destination_host, destination_port):
        result = None
        try:
            request = Request(
                networking=self,
                identifier = self.node.get_public_key_value(),
                action_json = {
                    "action_type": command.READY_TO_JOIN,
                    "host": self.node.host,
                    "port": self.node.port
                }
            )
            print(f"\nnetworking ready_to_join: destination_host: {destination_host}, destination_port: {destination_port}")
            print(f"request: {request.message.get_encoded_payload()}")
            result=await request.send_to(destination_host, destination_port)
        except Exception as e:
            print(f"Exception hit: {e}")
        return result

    async def resolve_source_inconsistency(self):
        print(f"networking: resolve source inconsistency")

    async def uptake_checkpoints(self):
        print(f"networking: uptake checkpoints")

    async def validate_nominations(self, nominee_count):
        print(f"\nvalidate_nominations: nominee_count: {nominee_count}")
        if self.node.directory.nominee_count() == nominee_count:
            try:
                print(f"Proceeding with validation...")
                self.node.directory.promote_nominations()
                size = self.node.directory.get_number_of_nodes()
                step = util.random_step(size)
                # iterate through n items
                print(f"Iterate through n items")
            except Exception as e:
                print(f"validate_nominations: hit exception: {e}")
        else:
            print(f"Discrepancy found: nominees found: {self.node.directory.nominee_count()}")

    def get_identifier(self):
        return self.node.checkpoint

    async def listen(self):
        print(f"\nlisten: port: {self.node.port}")
        listener = Listener(self)
        return await listener.run() 
