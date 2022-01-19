import asyncio

class EnvelopeHandler:

    def __init__(self, node):
        self.node = node

    async def handle_connection(self, reader, writer):
        # wait for message - nned to constrain by size
        data = await reader.readuntil(b"\n")
        print(f"Received: {data}")
        await writer.write("starting...\n".encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()


    async def run(self):
        return await asyncio.start_server(
	    self.handle_connection, 
            self.node.host, 
            self.node.port,
            limit = 10000
        )
