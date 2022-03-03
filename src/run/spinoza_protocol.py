"""
Protocol for validated broadcast to all nodes
"""

import json
from rpcudp.protocol import RPCProtocol

class Protocol(RPCProtocol):
    """
    Protocol is the class used for the validateable broadcast
    """

    def __init__(self, node, wait_timeout=10, protocol=None):
        RPCProtocol.__init__(self, wait_timeout=wait_timeout)
        self.node = node
        self.protocol = protocol
        self.messages_received = set()
        print(f"Protocol:__init__: node_id: {node.node_id}, host: {node.info.host}, port: {node.info.port}")

    def save_protocol_and_transport(self, protocol, transport):
        """
        save the protocol and transport
        """
        self.protocol = protocol
        self.transport = transport

    # If cached, return node receipt, otherwise generate and cache
    async def rpc_broadcast_to_node(self, address, message):
        """
        generate a receipt that the current node has received the message
        """
        #print(f"\nbroadcast_to_node: address: {address}, node_id: {self.node.node_id}")
        return self.node.get_node_receipt(message)

    async def rpc_broadcast_message_to_neighborhood(self, address, message):
        """
        broadcast the message to all the nodes in the current neighborhood
        """
        #print(f"\nrpc_broadcast_message_to_neighborhood: address: {address}")
        if self.node.has_receipt_for_current_neighborhood(message):
            return self.node.get_receipt_for_current_neighborhood(message)
        neighborhood_receipt = {}
        neighborhood_receipt[str(self.node.node_id)] = self.node.get_node_receipt(message)

        neighborhood = self.node.get_current_neighborhood()
        #print(f"\nrpc_broadcast_message_to_neighborhood: neighborhood: {neighborhood}")
        for node_info in neighborhood:
            node_address = (node_info['host'], node_info['port'])
            node_id = node_info['node_id']
            #print(f"\nnode_info: {node_info}, node_id: {node_info['node_id']},
            #      "node_address: {node_address}, current_node_id: {self.node.node_id}")
            # get node receipt
            # add to neighborhood receipt
            if node_id != self.node.node_id:
                result = await self.protocol.broadcast_to_node(node_address, message)
                neighborhood_receipt[str(node_id)] = result[1] if result[0] else None
        neighborhood_receipt = json.dumps(neighborhood_receipt)
        self.node.save_receipt_for_current_neighborhood(message, neighborhood_receipt)
        return neighborhood_receipt

    async def rpc_save_receipt_for_current_neighborhood(self, address, message,
                                                        neighborhood_receipt):
        """
        save the receipt for the current neighborhood to the current node
        """
        #print(f"\nrpc_save_receipt_for_current_neighborhood: address: {address}")
        self.node.save_receipt_for_current_neighborhood(message, neighborhood_receipt)

    async def rpc_save_receipt_for_next_neighborhood(self, address, message, neighborhood_receipt):
        """
        save the receipt for the next neighborhood to the current node
        """
        #print(f"\nrpc_save_receipt_for_next_neighborhood: address: {address}")
        self.node.save_receipt_for_next_neighborhood(message, neighborhood_receipt)

    async def rpc_broadcast_message_to_next_neighborhood(self, address, message, first_node_id,
                                                         last_node_id):
        """
        proceed to broadcast to the next neighborhood
        """
        #print(f"\nrpc_broadcast_message_to_next_neighborhood: address: {address}, first_node_id:"
        #      " {first_node_id}, last_node_id: {last_node_id}, node_id: {self.node.node_id}")

        receipt_for_current_neighborhood = (self.node.get_receipt_for_current_neighborhood(message)
            if self.node.has_receipt_for_current_neighborhood(message) else None)

        receipt_for_next_neighborhood = (self.node.get_receipt_for_next_neighborhood(message)
            if self.node.has_receipt_for_next_neighborhood(message) else None)

        current_neighborhood = self.node.get_current_neighborhood()
        #print(f"\nrpc_broadcast_message_to_next_neighborhood: node_id: {self.node.node_id}, "
        #      "current_neighborhood: {current_neighborhood}")

        # if needed, generate receipt for current neighborhood and save to all nodes
        if receipt_for_current_neighborhood is None:
            receipt_for_current_neighborhood = await self.rpc_broadcast_message_to_neighborhood(
                address, message)
            for node_info in current_neighborhood:
                address = (node_info['host'], node_info['port'])
                if node_info['node_id'] != self.node.node_id:
                    await self.protocol.save_receipt_for_current_neighborhood(
                        address, message, receipt_for_current_neighborhood)

        # if needed, generate receipt for next neighborhood and save to all nodes
        updated_first_node_id = (current_neighborhood[0]['node_id']
            if first_node_id is None else first_node_id)
        updated_last_node_id = self.node.get_updated_last_node_id(
            last_node_id if last_node_id is not None else 1)
        #print(f"\nnode_id: {self.node.node_id}, receipt_for_next_neighborhood: "
        #       "{receipt_for_next_neighborhood}")

        if (receipt_for_next_neighborhood is None and
            (first_node_id is None or first_node_id != last_node_id)):
            next_address = self.node.get_next_address()
            result = await self.protocol.broadcast_message_to_neighborhood(next_address, message)
            receipt_for_next_neighborhood = result[1] if result[0] else None
            for node_info in current_neighborhood:
                #print(f"\nnode_info: {node_info}, receipt_for_next_neighborhood: "
                #       "{receipt_for_next_neighborhood}")
                address = (node_info['host'], node_info['port'])
                if node_info['node_id'] != self.node.node_id:
                    await self.protocol.save_receipt_for_next_neighborhood(
                        address, message, receipt_for_next_neighborhood)
            self.node.save_receipt_for_next_neighborhood(message, receipt_for_next_neighborhood)

        # broadcast to next neighborhood if broadcast is not complete
        #print(f"\nchecking: first_id: {first_node_id}, last_id: {last_node_id},"
        #      " updated_first_id: {updated_first_node_id}, updated_last_id: "
        #      "{updated_last_node_id}")
        if first_node_id is None or first_node_id != last_node_id:
            next_address = self.node.get_next_address()
            #print(f"\nnode_id: {self.node.node_id}, next_address: {next_address}")
            await self.protocol.broadcast_message_to_next_neighborhood(next_address,
                      message, updated_first_node_id, updated_last_node_id)

        return (receipt_for_current_neighborhood, receipt_for_next_neighborhood)

    async def rpc_validate_next_broadcast(self, address, message, first_node_id, last_node_id):
        """
        proceed to validate each neighborhood, one neighborhood at a time
        """
        #print(f"\nrpc_validate_next_broadcast: address: {address}, node_id: {self.node.node_id},"
        #      " first_node_id: {first_node_id}, last_node_id: {last_node_id}")
        receipt_for_next_neighborhood = self.node.get_receipt_for_next_neighborhood(message)
        if receipt_for_next_neighborhood is None:
            print(f"\nrpc_validate_next_broadcast: node_id: {self.node.node_id},"
                  "Failed for receipt_for_next_neighborhood 1")
            return "Fail"
        if first_node_id is not None and first_node_id == last_node_id:
            return "Success"
        receipt_for_next_neighborhood = self.node.get_receipt_for_next_neighborhood(message)
        if receipt_for_next_neighborhood is None:
            print(f"\nrpc_validate_next_broadcast: node_id: {self.node.node_id},"
                  " Failed for receipt_for_next_neighborhood 2")
            return "Fail"
        next_node_id = int(list(json.loads(receipt_for_next_neighborhood))[0])
        #print(f"\nrpc_validate_broadcast: next_node_id: {next_node_id}")
        next_address = self.node.directory.get_address(next_node_id)
        last_node_id = next_node_id - 1 if next_node_id > 1 else 1
        return await self.protocol.validate_next_broadcast(next_address, message,
                                                           first_node_id, last_node_id)

    async def rpc_validate_broadcast(self, address, message):
        """
        validate that a broadcast was sent to all nodes
        """
        #print(f"\nrpc_validate_broadcast: address: {address}, message: {message},"
        #      " node_id: {self.node.node_id}")
        # 1. Validate current
        receipt_for_current_neighborhood = self.node.get_receipt_for_current_neighborhood(message)
        #print(f"\nprotocol:rpc_validate_broadcast: receipt_for_current_neighborhood:
        #      "{receipt_for_current_neighborhood}")
        #print(f"\nreceipt_for_current_neighborhood: {receipt_for_current_neighborhood}")
        if (receipt_for_current_neighborhood is None or
             self.node.found_invalid_neighborhood_receipt(
                 json.loads(receipt_for_current_neighborhood), message)):
            print(f"\nrpc_validate_broadcast: node_id: {self.node.node_id}, "
                   "receipt_for_current_neighborhood failed")
            return "Fail"

        # 2. Check next
        receipt_for_next_neighborhood = self.node.get_receipt_for_next_neighborhood(message)
        #print(f"\nreceipt_for_next_neighborhood: {receipt_for_next_neighborhood}")
        if (receipt_for_next_neighborhood is None or
            self.node.found_invalid_neighborhood_receipt(
                json.loads(receipt_for_next_neighborhood), message)):
            print(f"\nrpc_validate_broadcast: node_id: {self.node.node_id}, "
                  "receipt_for_next_neighborhood failed")
            return "Fail"

        next_node_id = int(list(json.loads(receipt_for_next_neighborhood))[0])
        first_node_id = int(list(json.loads(receipt_for_current_neighborhood))[0])
        #print(f"\nrpc_validate_broadcast: next_node_id: {next_node_id}")
        next_address = self.node.directory.get_address(next_node_id)
        last_node_id = next_node_id - 1 if next_node_id > 1 else 1
        return await self.protocol.validate_next_broadcast(next_address, message,
                                                           first_node_id, last_node_id)

    # Initiate a broadcast to all nodes
    #
    # Returns a dictionary of node_ids and receipts for the neighborhood of the address
    #
    # This neighborhood can be used to validate the broadcast
    async def rpc_initiate_broadcast(self, address, message):
        """
        initiate a broadcast to all nodes
        """

        # The initiator who calls this message needs to be registered
        # either through being a registered entity
        # or by having funds which can be spent on the broadcast.
        #
        # TODO: Add validation for initiator.
        #
        return await self.rpc_broadcast_message_to_next_neighborhood(address, message, None, None)
