from typing import Final
import os
import util

NODE_LIST_FILE: Final = "node_list.json"

class NodeList:

    def __init__(self, instance_path):
        if not os.path.exists(instance_path):
            util.create_directory_if_needed(instance_path)
        node_file = f"{instance_path}/{NODE_LIST_FILE}" 
        node_list = util.read_dict_from_file(node_file) if os.path.exists(node_file) else {}

    def add_validated_node(self, node):
        pass

    def persist(self):
        pass
