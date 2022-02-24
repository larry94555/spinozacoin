import asyncio
import json
from rpcudp.protocol import RPCProtocol
import time

start_time = time.time()

protocol_class = RPCProtocol(wait_timeout=100)
def _create_protocol():
    return protocol_class

loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(_create_protocol, local_addr=('127.0.0.1', 5090))
transport, protocol = loop.run_until_complete(listen)

request = {
    "message": {
        "action": "nominate_node",
        "host": "127.0.0.1",
        "port": "1234"
    }
}


async def broadcast_message(protocol, address, request):
    result = await protocol.broadcast_message(address, json.dumps(request))
    print(result[1] if result[0] else "No response received.")
    print(f"\ntime_elapsed: {time.time() - start_time}")

func = broadcast_message(protocol, ('127.0.0.1', 8889), request)
loop.run_until_complete(func)
loop.run_forever()
