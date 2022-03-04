"""
Networking api include server
"""

import asyncio
from spinoza_protocol import Protocol

class Server:
    """
    Server class used to start listener
    """
    NEIGHBORHOOD_SIZE=10

    def __init__(self, node):
        print(f"\nnode id: {node.node_id}, host: {node.info.host}, port: {node.info.port}")
        self.node = node
        self.protocol_class = Protocol(node, 5)

    def create_protocol(self):
        """
        create protocol
        """
        return self.protocol_class

    def listen(self, host, port):
        """
        have server listen to a host/port
        """
        print(f"Server.listen: host: {host}, port: {port}")
        loop = asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(self.create_protocol,
                                               local_addr=(host, port))
        transport, protocol = loop.run_until_complete(listen)
        self.protocol_class.save_protocol_and_transport(protocol=protocol, transport=transport)
