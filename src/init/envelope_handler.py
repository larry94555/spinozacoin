import asyncio

class EnvelopeHandler:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def handle_connection(self, reader, writer):
        # wait for message - nned to constrain by size
        data = await reader.readuntil(b"\n")
        await writer.write("starting...\n".encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()


    async def run(self):
        return await asyncio.start_server(self.handle_connection, self.host, self.port)
