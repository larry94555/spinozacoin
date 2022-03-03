"""
Node is the unit of the network
"""
import enum
import os

from node_directory import NodeDirectory
from node_receipts import NodeReceipts
from networking import Server
import util

class Status(enum.Enum):
    """
    Status values of a node
    """
    NEW = "status_new"
    DOWN = "status_down"
    UP = "status_up"
    UNRELIABLE = "status_unreliable"

class Node:
    """
    Node class for units of the network
    """
    NEIGHBORHOOD_SIZE = 15

    def __init__(self, node_info, node_id, status):
        self.info = node_info
        self.node_id = node_id
        self.status = status
        self.server = Server(self)
        self.directory = NodeDirectory(node_info.instance_path)
        self.receipts = NodeReceipts()
        #self.try_to_set_node_info()

    def found_invalid_neighborhood_receipt(self, neighborhood_receipt, message):
        """
        return true if invalid neighborhood receipt
        """
        #print(f"\nnode:found_invalid_neighborhood_receipt: message: {message}, "
        #      "neighborhood_receipt: {neighborhood_receipt}")
        return False in [self.validate_receipt(receipt[0], receipt[1],
                                               message) for receipt in neighborhood_receipt.items()]

    def get_current_neighborhood(self):
        """
        get current neighborhood
        """
        return self.directory.get_neighborhood(self.node_id, self.NEIGHBORHOOD_SIZE)

    def get_neighborhood_size(self):
        """
        get neighborhood size
        """
        return self.NEIGHBORHOOD_SIZE

    def get_next_address(self):
        """
        get next address
        """
        next_node_id = (self.node_id + self.NEIGHBORHOOD_SIZE if self.node_id +
                        self.NEIGHBORHOOD_SIZE <= self.directory.get_max_id() else self.node_id +
                        self.NEIGHBORHOOD_SIZE - self.directory.get_max_id())
        return self.directory.get_address(next_node_id)

    def get_next_neighborhood(self, start_id, last_id):
        """
        get next neighborhood
        """
        if last_id+1 == start_id or start_id == 1 and last_id == self.directory.get_max_id():
            return []
        next_last_id = last_id + self.NEIGHBORHOOD_SIZE
        if next_last_id > self.directory.get_max_id():
            next_last_id -= self.directory.get_max_id()
            if next_last_id > start_id:
                next_last_id = start_id - 1
        next_start_id = last_id + 1
        if next_start_id == self.directory.get_max_id():
            next_start_id = 1

        return self.directory.get_neighborhood_by_limits(next_start_id, next_last_id)

    def get_node_from_next_neighborhood(self):
        """
        get node from next neighborhood
        """
        return (self.node_id + self.NEIGHBORHOOD_SIZE) if (self.node_id +
                self.NEIGHBORHOOD_SIZE) <= self.directory.get_max_id() else (self.node_id +
                self.NEIGHBORHOOD_SIZE - self.directory.get_max_id())

    def get_node_receipt(self, message):
        """
        get node receipt
        """
        if message in self.receipts.receipts_for_node:
            return self.receipts.receipts_for_node[message]
        node_receipt = util.get_signature_for_json(
                           private_key=self.get_private_key(),
                           json_string=message).hex()
        # Test validate
        #print(f"\nNode: get_node_receipt: node_id: {self.node_id}, message: {message},"
        #      " node_receipt: {node_receipt}, validation: "
        #      "{self.validate_receipt(self.node_id, node_receipt, message)}")
        self.receipts.receipts_for_node[message] = node_receipt
        return node_receipt

    def get_receipt_for_current_neighborhood(self, message):
        """
        get receipt for current neighborhood
        """
        return self.receipts.receipts_for_current_neighborhood[message] if (message in
            self.receipts.receipts_for_current_neighborhood) else None

    def get_receipt_for_next_neighborhood(self, message):
        """
        get receipt for next neighborhood
        """
        return self.receipts.receipts_for_next_neighborhood[message] if (message in
            self.receipts.receipts_for_next_neighborhood) else None

    def get_public_key(self):
        """
        get public key
        """
        if self.receipts.get_public_key() is None or self.receipts.get_private_key() is None:
            if (not os.path.exists(self.info.private_key_file) or
                not os.path.exists(self.info.public_key_file)):
                self.receipts.create_secrets(self.info.private_key_file, self.info.public_key_file)
            self.receipts.set_public_key(
                util.get_public_key_from_serialized_value(self.info.public_key_file))
            self.receipts.set_private_key(
                util.get_private_key_from_serialized_value(self.info.private_key_file))
        return self.receipts.get_public_key()

    def get_private_key(self):
        """
        get private key
        """
        if self.receipts.get_private_key() is None:
            # generate new public_key which also generates private key
            self.receipts.get_public_key()
        return self.receipts.get_private_key()

    def get_updated_last_node_id(self, node_id):
        """
        get updated last node id
        """
        node_id += self.NEIGHBORHOOD_SIZE
        return 1 if node_id > self.directory.get_max_id() else node_id

    def has_receipt_for_current_neighborhood(self, message):
        """
        return true if has receipt for current neighborhood
        """
        return message in self.receipts.receipts_for_current_neighborhood

    def has_receipt_for_next_neighborhood(self, message):
        """
        return true if has receipt for next neighborhood
        """
        return message in self.receipts.receipts_for_next_neighborhood

    def listen(self):
        """
        listen for requests
        """
        print(f"node:listen: host: {self.info.host}, port: {self.info.port}")
        self.server.listen(host=self.info.host, port=self.info.port)

    def save_receipt_for_current_neighborhood(self, message, neighborhood_receipt):
        """
        save receipt for the current neighborhood
        """
        self.receipts.receipts_for_current_neighborhood[message] = neighborhood_receipt

    def save_receipt_for_next_neighborhood(self, message, neighborhood_receipt):
        """
        save receipt for the next neighborhood
        """
        self.receipts.receipts_for_next_neighborhood[message] = neighborhood_receipt

    def try_to_set_node_info(self):
        """
        set node_info if it has been persisted
        """
        if os.path.exists(self.info.get_node_id_file()):
            self.node_id = util.read_num_from_file(self.info.get_node_id_file())
            self.directory.set_node_info(self)

    def validate_node_down(self, node_id):
        """
        validate that a node is down
        """
        return node_id is not None

    def validate_receipt(self, node_id, receipt, message):
        """
        validate that the receipt was signed by the node_id
        """
        #print(f"\nnode.validate_receipt: node_id: {node_id}, receipt: {receipt}")
        public_key = self.directory.get_public_key(node_id)
        result=self.validate_node_down(node_id) if receipt == "down" else util.validate_signature(
            public_key_hex=public_key, signature_hex=receipt, json_string=message)
        #if result == False:
        #    print(f"\n***Fail: Node: validate_receipt: node_id: {node_id}, message: "
        #          "{message}, node_receipt: {receipt},")
        #else:
        #    print(f"\nPassed: Node: validate_receipt: node_id: {node_id}, message: "
        #          "{message}, node_receipt: {receipt},")
        return result
