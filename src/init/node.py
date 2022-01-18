from networking import Networking
import os
import util

class Node:

    def __init__(self, instance_id, config, loop):
        self.instance_id = instance_id
        self.host = config.get_host()
        self.port = config.get_base_port() + instance_id
        self.config = config
        self.loop = loop
        self.networking = Networking(self)

    def create_secrets(self, private_key_file, public_key_file):
        self.private_key_value, self.public_key_value = util.generate_private_and_public_keys()
        util.write_string_to_file(self.private_key_value, private_key_file)
        util.write_string_to_file(self.public_key_value, public_key_file)

    def initialize(self):
        # Create secrets if not already created
        secrets_path = f"{self.config.get_instance_base_path()}/instance{self.instance_id}/secrets"
        util.create_directory_if_needed(secrets_path)
        private_key_file = f"{secrets_path}/node.private.key"
        public_key_file = f"{secrets_path}/node.public.key"
        print(f"secrets_path: {secrets_path}")
        if not (os.path.exists(private_key_file) and os.path.exists(public_key_file)):
            print("Creating new secret")
            self.create_secrets(private_key_file, public_key_file)
        else:
            print("Secret already exists")
            self.private_key_value = util.read_string_from_file(public_key_file)
            self.public_key_value = util.read_string_from_file(private_key_file)

    async def start_node(self):
        if self.config.get_trusted_node() != "127.0.0.1" or self.instance_id != 0:
            await self.networking.announce_to(self.config.get_trusted_node(), self.config.get_trusted_port())

        server = await self.networking.listen()
        print(f"Node started: {self.config.get_trusted_node()}:{self.instance_id+self.config.get_base_port()}")
        return server 
    
    async def join_network(self):
        self.initialize()
        return await self.start_node()

