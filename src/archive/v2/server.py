import asyncio
import config
import enum
from typing import Final
from node_directory import NodeDirectory
import os
import util

class Status(enum.Enum):
    new = "status_new"
    down = "status_down"
    up = "status_up"
    unreliable = "status_unreliable"

class Server:

    def __init__(self, instance_id, config, loop):
        self.instance_id = instance_id
        self.host = config.get_host()
        self.port = config.get_base_port() + instance_id
        self.config = config
        self.loop = loop
        self.directory = NodeDirectory(config.instance_path)
        self.checkpoint_file = f"{config.instance_path}/checkpoint.txt"
        self.checkpoint = None
        self.status = None
        self.open_to_nominations = True
        self.try_to_set_node_info()

    def get_private_key(self):
        return util.get_private_key_from_serialized_value(self.get_private_key_serialized_value())

    def get_private_key_serialized_value(self):
        return util.read_bytes_from_file(f"{self.config.instance_path}/instance{self.instance_id}/secrets/node.private.key.pem")

    def get_public_key_serialized_value(self):
        return util.read_bytes_from_file(f"{self.config.instance_path}/instance{self.instance_id}/secrets/node.public.key.pem")

    def get_public_key_value(self):
        return util.get_public_key_value_from_serialized_value(self.get_public_key_serialized_value()) 

    def listen(self):
        pass

    def restart_registered_node(self):
        self.status = Status.down

    def run(self):
        if self.config.get_trusted_node() == "127.0.0.1" and self.instance_id == 0:
            # start first node
            self.start_first_node()
        elif self.checkpoint == None:
            # start new node
            self.start_new_node()
        else:
            # bring back online registered node
            self.restart_registered_node()
        self.listen()

    def start_first_node(self):
        if self.checkpoint == None:
            self.checkpoint=1
            self.directory.add_checkpoint([self],0)
            self.directory.persist()
            util.write_num_to_file(self.checkpoint, self.checkpoint_file)

    def start_new_node(self):
        self.status = Status.new

    def try_to_set_node_info(self):
        if os.path.exists(self.checkpoint_file):
            self.checkpoint = util.read_num_from_file(self.checkpoint_file)
            self.directory.set_node_info(self)
