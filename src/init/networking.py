import command
from envelope import Envelope
from envelope_handler import EnvelopeHandler
import util

class Networking:

    def __init__(self, node):
        self.node = node
        self.alias = util.generate_alias()

    async def announce_to(self, destination_host, destination_port):
        envelope = Envelope(
            node=self.node,
            identifier = self.node.get_public_key_value(),
            action=command.ANNOUNCE, 
            action_details={ "alias": self.alias }
        )
        return await envelope.send_to(destination_host, destination_port)

    async def listen(self):
        envelopeHandler = EnvelopeHandler(self.node)
        return await envelopeHandler.run() 
