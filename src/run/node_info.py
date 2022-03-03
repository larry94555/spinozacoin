"""
NodeInfo: a pojo for node information
"""

import util

class NodeInfo:
    """
    Main class for node information
    """

    NODE_ID_FILENAME = "node_id.txt"


    def __init__(self, instance_id, host, port, instance_path):
        self.instance_id = instance_id
        self.host = host
        self.port = port
        self.instance_path = util.create_path_if_needed(instance_path)
        self.secrets_path = util.create_path_if_needed(f"{instance_path}/secrets")
        self.private_key_file = f"{self.secrets_path}/node.private.key.pem"
        self.public_key_file = f"{self.secrets_path}/node.public.key.pem"

    def get_address(self):
        """
        return address for given node_info
        """
        return (self.host, self.port)

    def get_node_id_file(self):
        """
        get node id file
        """
        return f"{self.instance_path}/{self.NODE_ID_FILENAME}"
