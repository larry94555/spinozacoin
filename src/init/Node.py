import asyncio
from client import Client
import os
import util

async def handle_connection(reader, writer):
    # wait for message - nned to constrain by size
    data = await reader.readuntil(b"\n")
    await writer.write("starting...\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

class Node:

    def __init__(self, instanceId, config, loop):
        self.validate_config(config)
        self.instanceId = instanceId
        self.countDeadInstances = config['countDeadInstances']
        self.instanceBasePath = os.path.expanduser(config['instanceBasePath'])
        self.trustedNode = config['trustedNode']
        self.trustedPort = config['trustedPort']
        self.basePort = config['port']
        self.loop = loop

    def validate_config(self, config):
        for property in ['countDeadInstances', 'instanceBasePath', 'trustedNode', 'trustedPort', 'port']:
            if property not in config:
                print(f"A required property in the configuration file is missing: {property}")
                exit()


    def create_secrets(self, secretsPath):
        privateKeyValue, publicKeyValue = util.generate_private_and_public_keys()
        util.create_directory_if_needed(secretsPath)
        util.write_string_to_file(privateKeyValue, f"{secretsPath}/node.private.key")
        util.write_string_to_file(publicKeyValue, f"{secretsPath}/node.public.key")

    def initialize(self):
        # Create secrets if not already created
        instanceSecretsPath = f"{self.instanceBasePath}/instance{self.instanceId}/secrets"
        if not os.path.exists(f"{instanceSecretsPath}/node.private.key") or not os.path.exists("{instanceSecretsPath}/node.public.key"):
            self.create_secrets(instanceSecretsPath)

    async def register_with_trusted_node(self):
        message = f"test: {self.trustedNode}:{self.trustedPort}"
        host = self.trustedNode
        print(f"handle_register connecting_to: host: {host}, port: {self.trustedPort}")
        try:
            transport, protocol = await self.loop.create_connection(Client,host=host, port = self.trustedPort)
            print(f"client connection succeeded: {message}")
            transport.write(f"{message}\n".encode())
            print(f"message sent... waiting for reply")
        except Exception as e:
            print(f"Connection to {host}:{port} failed with error: {e}")

    async def start_node(self):
        if self.trustedNode != "127.0.0.1" or self.instanceId != 0:
            await self.register_with_trusted_node()

        server = await asyncio.start_server(handle_connection, self.trustedNode, self.basePort + self.instanceId)
        print(f"Node started: {self.trustedNode}:{self.instanceId+self.basePort}")
        return server 
    
    async def join_network(self):
        self.initialize()
        return await self.start_node()
        
        
