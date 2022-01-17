import commands
from envelope import Envelope
from envelope_handler import EnvelopeHandler

class Networking:

    def __init__(self, instanceId, host, port, loop):
        self.loop = loop
        self.instanceId = instanceId
        self.host = host
        self.port = port

    async def announce_to(self, destinationHost, destinationPort):
        envelope = Envelope(self.instanceId, self.host, self.port, self.loop)
        return await envelope.sendTo(destinationHost, destinationPort, commands.ANNOUNCE)

    async def listen(self):
        envelopeHandler = EnvelopeHandler(self.host, self.port)
        return await envelopeHandler.run() 
