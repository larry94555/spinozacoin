import asyncio
import json
from rpcudp.protocol import RPCProtocol
import util

class Protocol(RPCProtocol):

    def __init__(self, node, wait_timeout=10, protocol=None):
        RPCProtocol.__init__(self, wait_timeout=wait_timeout)
        self.node = node
        self.protocol = protocol
        self.messages_received = set()
        print(f"Protocol:__init__: node_id: {node.node_id}, host: {node.host}, port: {node.port}")

    def save_protocol_and_transport(self, protocol, transport):
        self.protocol = protocol
        self.transport = transport

    def already_handled(self, id, start_id, last_id):
        if start_id is None:
            return False
        elif start_id <= last_id:
            return id >= start_id and id <= last_id
        elif last_id < start_id:
            max_id = self.node.directory.get_max_id()
            return (id >= start_id and id <= max_id or
                    id <= last_id)
        else:
            print(f"Unexpected state")
            return False

    async def rpc_broadcast_message_to_next_neighborhood(self, address, message, start_id, last_id, source_node):
        if source_node <= 10:
            #print(f"\nProtoocol:rpc_broadcast_message_to_next_neighborhood: source_node: {source_node}, for: node_id: {self.node.node_id}, from: {address}, message: {message}, start_id: {start_id}, last_id: {last_id}")
            pass

        # Skip if already received
        if self.node.already_received(message):
            if source_node in [1,2]:
                #print(f"\nreturning check...: source_node: {source_node}, node_id: {self.node.node_id}, saved: {self.node.get_saved_message(message)}") 
                pass
            check=json.dumps(self.node.get_saved_message(message))
            return check

        saved_response = {}
        next_neighborhood = self.node.get_next_neighborhood(start_id, last_id)
        # each node does the broadcast and the resulting node rejects if it has alrady received the message
     
        next_last_id = next_neighborhood[-1]['node_id'] if len(next_neighborhood) > 0 else None
        for node_info in next_neighborhood:
            #print(f"\nnode_id: {node_info['node_id']}, host: {node_info['host']}, port: {node_info['port']}")
            result = await self.protocol.broadcast_message_to_next_neighborhood( 
                (node_info['host'], node_info['port']),
                message, start_id, next_last_id, self.node.node_id)
            if result[0] and result[1] is not None:
                if self.node.node_id in [1,2]:
                    #print(f"\nnode_id: {self.node.node_id}, result[1]: {result[1]}")
                    pass
                saved_response |= json.loads(result[1])

        response = {}
        response[str(self.node.node_id)] = util.get_signature_for_json(
                                                  private_key=self.node.get_private_key(),
                                                  json_string=json.dumps(message)).hex()
        if len(saved_response)==0:
            #print(f"\nnode_id: {self.node.node_id}, response: {response}")
            self.node.save_message(message, response) 
        else:
            #print(f"\nnode_id: {self.node.node_id}, saved_response: {saved_response}")
            self.node.save_validation(message, saved_response)
        #print(f"\nnode_id {self.node.node_id}, saved_response: {saved_response}")
        if source_node==2:
            #print(f"\nsource_node: {source_node}, node_id: {self.node.node_id}, response: {response}")
            pass

        self.node.save_message(message, response)
        return json.dumps(response)

    async def rpc_broadcast_message(self, address, message, start_id=None, last_id=None):
        print(f"\nProtocol:rpc_broadcast_message: current: host: {self.node.host}, port: {self.node.port}, from: {address}, message: {message}, start_id: {start_id}, last_id: {last_id}") 

        # 2 cases to handle
        # case 1: last_id >= start_id: between start_id and last_id
        # case 2: last_id < start_id: between start_id and end or first and last_id
        #
        # Generate receipts for each node in neighborhood
        response = {}
        neighborhood = self.node.get_current_neighborhood()
        print(f"\nCurrent Neighborhood: length: {len(neighborhood)}")
        next_start_id = neighborhood[0]['node_id']
        next_last_id = neighborhood[-1]["node_id"]
        response[str(self.node.node_id)] = util.get_signature_for_json(
                                                  private_key=self.node.get_private_key(),
                                                  json_string=json.dumps(message)).hex()
        for node_info in neighborhood:
            print(f"node_id: {node_info['node_id']}, host: {node_info['host']}, port: {node_info['port']}")
            result = await self.protocol.broadcast_message_to_next_neighborhood((node_info['host'], node_info['port']), message, next_start_id, next_last_id, self.node.node_id)
            if result[0] and result[1] is not None:
                response |= json.loads(result[1])
        
        #print(f"\nresponse: {response}") 
        return json.dumps(response)
