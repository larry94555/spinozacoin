import commands
from envelope import Envelope
from envelope_handler import EnvelopeHandler

class Networking:

    def __init__(self, node):
        self.node = node

    async def announce_to(self, destination_host, destination_port):
        envelope = Envelope(self.node)
        return await envelope.send_to(destination_host, destination_port, commands.ANNOUNCE)

    async def listen(self):
        envelopeHandler = EnvelopeHandler(self.node)
        return await envelopeHandler.run() 
