import asyncio
from rpcudp import RPCProtocol

class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_sayhi(self, sender, name):
        print(f"rpc_sayhi: sender: {sender}, name: {name}")
        return f"Hello {name} you live at {sender[0]}:{sender[1]}"

# Start a server on udp port 1234
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCServer, local_addr=('127.0.0.1', 1234))
transport, protocol = loop.run_until_complete(listen)
loop.run_forever()
