import asyncio
import enum
import json
from node_directory import NodeDirectory
import os
from networking import Server
import util

class Status(enum.Enum):
    new = "status_new"
    down = "status_down"
    up = "status_up"
    unreliable = "status_unreliable"

class Node:

    NODE_ID_FILENAME = "node_id.txt"
    NEIGHBORHOOD_SIZE = 15
    
    def __init__(self, instance_id, instance_path, host, port, status=None, node_id=None):
        print(f"Node.__init__: instance_id: {instance_id}, instance_path: {instance_path}, host: {host}, port: {port}, status: {status}")
        self.instance_id = instance_id
        self.host = host
        self.port = port
        self.instance_path = instance_path
        self.node_id = node_id
        self.status = status
        self.server = Server(self)
        self.__public_key = None
        self.__private_key = None
        self.directory = NodeDirectory(instance_path)
        self.instance_path = self.create_path_if_needed(instance_path)
        self.secrets_path = self.create_path_if_needed(f"{instance_path}/secrets")
        self.private_key_file = f"{self.secrets_path}/node.private.key.pem"
        self.public_key_file = f"{self.secrets_path}/node.public.key.pem"
        self.try_to_set_node_info()
        self.receipts_for_node = {}
        self.receipts_for_current_neighborhood = {}
        self.receipts_for_next_neighborhood = {}

    def create_path_if_needed(self, path):
        if not os.path.exists(path):
            util.create_directory_if_needed(path)
        return path

    def create_secrets(self):
        private_key, public_key = util.generate_private_and_public_keys()
        util.write_bytes_to_file(private_key, self.private_key_file)
        util.write_bytes_to_file(public_key, self.public_key_file)

    def found_invalid_neighborhood_receipt(self, neighborhood_receipt, message):
        #print(f"\nnode:found_invalid_neighborhood_receipt: message: {message}, neighborhood_receipt: {neighborhood_receipt}")
        return False in [self.validate_receipt(receipt[0], receipt[1], message) for receipt in neighborhood_receipt.items()]

    def get_current_neighborhood(self):
        return self.directory.get_neighborhood(self.node_id, self.NEIGHBORHOOD_SIZE)

    def get_neighborhood_size(self):
        return self.NEIGHBORHOOD_SIZE

    def get_next_address(self):
        next_node_id = self.node_id + self.NEIGHBORHOOD_SIZE if self.node_id + self.NEIGHBORHOOD_SIZE <= self.directory.get_max_id() else self.node_id + self.NEIGHBORHOOD_SIZE - self.directory.get_max_id()
        node_info = self.directory.get_node_info(next_node_id)
        return (node_info['host'], node_info['port'])

    def get_next_neighborhood(self, start_id, last_id):
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
        return self.node_id + self.NEIGHBORHOOD_SIZE if self.node_id + self.NEIGHBORHOOD_SIZE <= self.directory.get_max_id() else self.node_id + self.NEIGHBORHOOD_SIZE - self.directory.get_max_id()

    def get_node_id_file(self):
        return f"{self.instance_path}/{self.NODE_ID_FILENAME}"

    def get_node_receipt(self, message):
        if message in self.receipts_for_node:
            return self.receipts_for_node[message]
        node_receipt = util.get_signature_for_json(
                           private_key=self.get_private_key(),
                           json_string=message).hex()
        # Test validate
        #print(f"\nNode: get_node_receipt: node_id: {self.node_id}, message: {message}, node_receipt: {node_receipt}, validation: {self.validate_receipt(self.node_id, node_receipt, message)}")
        self.receipts_for_node[message] = node_receipt
        return node_receipt

    def get_receipt_for_current_neighborhood(self, message):
        return self.receipts_for_current_neighborhood[message] if message in self.receipts_for_current_neighborhood else None

    def get_receipt_for_next_neighborhood(self, message):
        return self.receipts_for_next_neighborhood[message] if message in self.receipts_for_next_neighborhood else None

    def get_public_key(self):
        if self.__public_key is None or self.__private_key is None:
            if not os.path.exists(self.private_key_file) or not os.path.exists(self.public_key_file):
                 self.create_secrets()
            self.__public_key = util.get_public_key_from_serialized_value(self.public_key_file)
            self.__private_key = util.get_private_key_from_serialized_value(self.private_key_file)
        return self.__public_key

    def get_private_key(self):
        if self.__private_key is None:
            # generate new public_key which also generates private key
            self.get_public_key()
        return self.__private_key

    def get_saved_message(self, message):
        return self.messages_received[message]

    def get_updated_last_node_id(self, node_id):
        node_id += self.NEIGHBORHOOD_SIZE
        return 1 if node_id > self.directory.get_max_id() else node_id

    def has_receipt_for_current_neighborhood(self, message):
        return message in self.receipts_for_current_neighborhood

    def has_receipt_for_next_neighborhood(self, message):
        return message in self.receipts_for_next_neighborhood
        
    def listen(self):
        print(f"node:listen: host: {self.host}, port: {self.port}")
        self.server.listen(host=self.host, port=self.port)

    def save_receipt_for_current_neighborhood(self, message, neighborhood_receipt):
        self.receipts_for_current_neighborhood[message] = neighborhood_receipt

    def save_receipt_for_next_neighborhood(self, message, neighborhood_receipt):
        self.receipts_for_next_neighborhood[message] = neighborhood_receipt

    def try_to_set_node_info(self):
        if os.path.exists(self.get_node_id_file()):
            self.node_id = util.read_num_from_file(self.get_node_id_file())
            self.directory.set_node_info(self)

    def validate_node_down(self, node_id):
        return True

    def validate_receipt(self, node_id, receipt, message):
        #print(f"\nnode.validate_receipt: node_id: {node_id}, receipt: {receipt}")
        public_key = self.directory.get_public_key(node_id)
        result=self.validate_node_down(node_id) if receipt == "down" else util.validate_signature(public_key_hex=public_key, signature_hex=receipt, json_string=message)
        #if result == False:
        #    print(f"\n***Fail: Node: validate_receipt: node_id: {node_id}, message: {message}, node_receipt: {receipt},")
        #else:
        #    print(f"\nPassed: Node: validate_receipt: node_id: {node_id}, message: {message}, node_receipt: {receipt},")
        return result