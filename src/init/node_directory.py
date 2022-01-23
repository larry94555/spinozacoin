from typing import Final
import os
import util

NODE_BACKUP_HISTORY: Final = 1
NODE_DIRECTORY_FILE: Final = "node_directory.json"

class NodeDirectory:

    def __init__(self, instance_path):
        if not os.path.exists(instance_path):
            util.create_directory_if_needed(instance_path)
        self.node_file = f"{instance_path}/{NODE_DIRECTORY_FILE}" 
        self.node_directory = util.read_dict_from_file(self.node_file) if os.path.exists(self.node_file) else {}

    def add_node(self, node):
        self.node_directory[node.checkpoint] = self.get_node_info(node)

    def add_checkpoint(self, node_list, base_checkpoint):
        for i, node in enumerate(sorted(node_list, key=lambda x: f"{x.host}:{x.port}")):
            node.checkpoint = base_checkpoint + i + 1
            self.add_node(node)
        
    def get_latest_checkpoint(self):
        return len(self.node_directory)

    def get_node_info(self, node):
        return {
            "checkpoint": node.checkpoint,
            "public_key": node.get_public_key_value(),
            "host": node.host,
            "port": node.port,
            "status": node.status
        }

    def has_checkpoint(self, checkpoint):
        return checkpoint in self.node_directory

    def up_to_n(self, num_nodes_returned, start_pos, step, offset, size):
        if (n := min(num_nodes_returned,size - offset)) == 0:
            return []
        n_nodes = []
        start_adjusted = (start_pos + offset*step) % size + 1
        for i in range(n):
            i_adjusted = (start_adjusted + (i-1)*step) % size + 1
            n_nodes.append(self.node_directory[str(i_adjusted)])
        return n_nodes
        
    def persist(self):
        util.backup_file(self.node_file,NODE_BACKUP_HISTORY)
        util.write_dict_to_file(self.node_directory, self.node_file) 

    def set_node_info(self, node):
        if self.has_checkpoint(node.checkpoint):
            entry = self.node_directory.get(node.checkpoint)
            node.status = entry.status
