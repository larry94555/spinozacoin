import node_directory
from typing import Final
from node_directory import NodeDirectory
from networking import Networking
import os
import util

CHECKPOINT_FILENAME: Final = "checkpoint.txt"

class Node:

    # status:  None (initialization)
    #          New (if starting for the first time)
    #          Down (if have checkpoint assigned)
    #          Up (after validation) 
    def __init__(self, instance_id, config, loop):
        self.instance_id = instance_id
        self.host = config.get_host()
        self.port = config.get_base_port() + instance_id
        self.config = config
        self.loop = loop
        self.checkpoint = None
        self.status = None
        self.networking = Networking(self)
        self.directory = NodeDirectory(self.get_instance_path())
        self.try_to_set_node_info()

    def create_secrets(self, private_key_file, public_key_file):
        serialized_private_key, serialized_public_key = util.generate_private_and_public_keys()
        util.write_bytes_to_file(serialized_private_key, private_key_file)
        util.write_bytes_to_file(serialized_public_key, public_key_file)

    def get_checkpoint_file(self):
        return f"{self.get_instance_path()}/{CHECKPOINT_FILENAME}"

    def get_instance_path(self):
        return f"{self.config.get_instance_base_path()}/instance{self.instance_id}"

    def get_node_directory_file(self):
        return f"{self.get_instance_path()}/{node_directory.NODE_DIRECTORY_FILE}"

    def get_secrets_path(self):
        return f"{self.get_instance_path()}/secrets"

    def get_private_key_file(self):
        return f"{self.get_secrets_path()}/node.private.key.pem"

    def get_public_key_file(self):
        return f"{self.get_secrets_path()}/node.public.key.pem"

    def get_private_key(self):
        return util.get_private_key_from_serialized_value(self.get_private_key_serialized_value())

    def get_public_key_serialized_value(self):
        return util.read_bytes_from_file(self.get_public_key_file()) 

    def get_private_key_serialized_value(self):
        return util.read_bytes_from_file(self.get_private_key_file())

    def get_public_key_value(self):
        return util.get_public_key_value_from_serialized_value(self.get_public_key_serialized_value())

    def handle_first_node(self):
        self.status="up"
        if not os.path.exists(self.get_node_directory_file()):
            self.checkpoint=1
            self.directory.add_checkpoint([self],0) 
            self.directory.persist()
        if not os.path.exists(self.get_checkpoint_file()):
            self.checkpoint=1
            self.persist()
      
    def initialize(self):
        # Create secrets if not already created
        print(f"secrets_path: {self.get_secrets_path()}")
        util.create_directory_if_needed(self.get_secrets_path())
        if not (os.path.exists(self.get_private_key_file()) and os.path.exists(self.get_public_key_file())):
            print("Creating new secret")
            self.create_secrets(self.get_private_key_file(), self.get_public_key_file())
        else:
            print("Secret already exists")

    async def join_network(self):
        self.initialize()
        return await self.start_node()

    def persist(self):
        if self.checkpoint != None:
            util.write_num_to_file(self.checkpoint, self.get_checkpoint_file())

    async def start_node(self):
        if self.config.get_trusted_node() != "127.0.0.1" or self.instance_id != 0:
            self.status="new" if self.checkpoint == None else "down"
            await self.networking.announce_to(self.config.get_trusted_node(), self.config.get_trusted_port())
        else:
            self.handle_first_node()
        print(f"\nstart_node: port: {self.port}, status: {self.status}")

        return await self.networking.listen()
    
    def try_to_set_node_info(self):
        if os.path.exists(self.get_checkpoint_file()):
            self.checkpoint = util.read_num_from_file(self.get_checkpoint_file()) 
            self.directory.set_node_info(self)


