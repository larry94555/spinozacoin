from networking import Networking
import os
import util

class Node:

    def __init__(self, instanceId, config, loop):
        self.validate_config(config)
        self.instanceId = instanceId
        self.countDeadInstances = config['countDeadInstances']
        self.instanceBasePath = os.path.expanduser(config['instanceBasePath'])
        self.trustedNode = config['trustedNode']
        self.trustedPort = config['trustedPort']
        self.basePort = config['port']
        self.networking = Networking(instanceId, "127.0.0.1", instanceId + self.basePort, loop)

    def validate_config(self, config):
        for property in ['countDeadInstances', 'instanceBasePath', 'trustedNode', 'trustedPort', 'port']:
            if property not in config:
                print(f"A required property in the configuration file is missing: {property}")
                exit()


    def create_secrets(self, secretsPath):
        self.privateKeyValue, self.publicKeyValue = util.generate_private_and_public_keys()
        util.create_directory_if_needed(secretsPath)
        util.write_string_to_file(self.privateKeyValue, f"{secretsPath}/node.private.key")
        util.write_string_to_file(self.publicKeyValue, f"{secretsPath}/node.public.key")

    def initialize(self):
        print("Initialize")
        # Create secrets if not already created
        secretsPath = f"{self.instanceBasePath}/instance{self.instanceId}/secrets"
        print(f"secretsPath: {secretsPath}")
        if not (os.path.exists(f"{secretsPath}/node.private.key") and os.path.exists(f"{secretsPath}/node.public.key")):
            print("Create secrets")
            self.create_secrets(secretsPath)
        else:
            print("Not create secrets")
            self.privateKeyValue = util.read_string_from_file(f"{secretsPath}/node.private.key")
            self.publicKeyValue = util.read_string_from_file(f"{secretsPath}/node.public.key")

    async def start_node(self):
        if self.trustedNode != "127.0.0.1" or self.instanceId != 0:
            await self.networking.announce_to(self.trustedNode, self.trustedPort)

        server = await self.networking.listen()
        print(f"Node started: {self.trustedNode}:{self.instanceId+self.basePort}")
        return server 
    
    async def join_network(self):
        self.initialize()
        return await self.start_node()

