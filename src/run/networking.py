import asyncio
from protocol import Protocol

class Server:

    NEIGHBORHOOD_SIZE=10

    def __init__(self, node):
        print(f"\nnode id: {node.node_id}, host: {node.host}, port: {node.port}")
        self.node = node
        self.protocol_class = None
        self.protocol_class = Protocol(node, 100)

    def _create_protocol(self):
        return self.protocol_class

    def listen(self, host, port):
        print(f"Server.listen: host: {host}, port: {port}")
        loop = asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(self._create_protocol,
                                               local_addr=(host, port))
        transport, protocol = loop.run_until_complete(listen)
        self.protocol_class.save_protocol_and_transport(protocol=protocol, transport=transport)
        
