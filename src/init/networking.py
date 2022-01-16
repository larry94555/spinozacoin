import asyncio
from client import Client

async def handle_connection(reader, writer):
    # wait for message - nned to constrain by size
    data = await reader.readuntil(b"\n")
    await writer.write("starting...\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

class Networking:

    def __init__(self, loop):
        self.loop = loop

    async def register_with_node(self, host, port):
        message = f"test: {host}:{port}"
        print(f"handle_register connecting_to: host: {host}, port: {port}")
        try:
            transport, protocol = await self.loop.create_connection(Client,host=host, port = port)
            print(f"client connection succeeded: {message}")
            # This should be a command such as #send_node_info
            transport.write(f"{message}\n".encode())
            print(f"message sent... waiting for reply")
        except Exception as e:
            print(f"Connection to {host}:{port} failed with error: {e}")

    async def listen(self, host, port):
        return await asyncio.start_server(handle_connection, host, port)
