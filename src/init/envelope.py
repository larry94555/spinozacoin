from client import Client

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

class Envelope:
 
    # synchronize on a file for now 
    def __init__(self, node):
        self.node = node

    def build_envelope(self):
        pass

    async def handle_connection(self, reader, writer):
        # wait for message - nned to constrain by size
        data = await reader.readuntil(b"\n")
        await writer.write("starting...\n".encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

    async def send_to(self, destination_host, destination_port, command):
        # build
        message = f"test: {destination_host}:{destination_port}"
        print(f"announce_to_node connecting_to: host: {destination_host}, port: {destination_port}")
        try:
            transport, protocol = await self.node.loop.create_connection(Client,host=destination_host, port = destination_port)
            print(f"client connection succeeded: {message}")
            # This should be a command such as #send_node_info
            transport.write(f"{message}\n".encode())
            print(f"message sent... waiting for reply")
        except Exception as e:
            print(f"Connection to {destination_host}:{destination_port} failed with error: {e}")
    
