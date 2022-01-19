import asyncio
import command
from typing import Final
import util

# the envelope has two parts:
# outer envelope:  Hash, Checksum, Pow
# inner envelope:  Signed by PrivateKey, Timestamp, OrderId
# command
# the goal is to wrap a command in the envelope which signifies:
# * the source of the message received
# * pow that shows that source understands the protocol
# * maximum size allowed, if size greater than max bytes, then close the connection
#
# Envelope is always for source when being built and always for the destination when being parsed

SPINOZA_COIN_PREFIX: Final = b'\x02\x03\x05\x07'
SPINOZA_COIN_SUFFIX: Final = b'\x07\x07\x07\x07'

class EnvelopeClientProtocol(asyncio.Protocol):
    def __init__(self, envelope, loop):
        self.envelope = envelope
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

class Envelope:
 
    # synchronize on a file for now 
    def __init__(self, node, identifier, action, action_details=None):
        self.node = node
        sequence_id = self.next_id()
        timestamp = self.timestamp()
        encrypted_action = util.encrypt_action(
            private_key_value = node.get_private_key_value(),
	    sequence_id=sequence_id, 
	    timestamp=timestamp, 
            action=action,
            action_details=action_details
        )
        self.encoded_payload = self.build_encoded_payload(
	    prefix=SPINOZA_COIN_PREFIX,
            identifier=identifier,
            encrypted_action = encrypted_action
        )

    def next_id(self):
        return 1

    def timestamp(self):
        return 0

    def build_encoded_payload(self, prefix, identifier, encrypted_action):
        return b"This is a test\n"

    async def send_to(self, destination_host, destination_port):
        # build
        try:
            transport, protocol = await self.node.loop.create_connection(lambda: EnvelopeClientProtocol(self, self.node.loop), host=destination_host, port = destination_port)
            # This should be a command such as #send_node_info
            transport.write(self.encoded_payload)
            # There should always be a return envelope
            
        except Exception as e:
            print(f"Connection to {destination_host}:{destination_port} failed with error: {e}")
    
