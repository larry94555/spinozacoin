import command
from envelope import Envelope
from envelope_handler import EnvelopeHandler
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
        envelope = Envelope(
            networking=self,
            identifier = self.node.get_public_key_value(),
            action=command.ANNOUNCE, 
            action_details={ 
                "host": self.node.host,
                "port": self.node.port
            }
        )
        return await envelope.send_to(destination_host, destination_port)

    async def listen(self):
        envelope_handler = EnvelopeHandler(self)
        return await envelope_handler.run() 
