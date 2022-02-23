import asyncio
import json
from rpcudp.protocol import RPCProtocol

loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', 8889))
transport, protocol = loop.run_until_complete(listen)

request = {
    "action": "broadcast",
    "message": "test"
}

async def broadcast_message(protocol, address, request):
    result = await protocol.broadcast_message(address, json.dumps(request))
    print(result[1] if result[0] else "No response received.")


func = broadcast_message(protocol, ('127.0.0.1', 8888), request)
loop.run_until_complete(func)
loop.run_forever()
