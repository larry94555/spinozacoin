from typing import Final
import os
import random
import util

NODE_BACKUP_HISTORY: Final = 1
NODE_DIRECTORY_FILE: Final = "node_directory.json"
DEFAULT_HASH: Final = "007"

class NodeDirectory:

    def __init__(self, instance_path):
        if not os.path.exists(instance_path):
            util.create_directory_if_needed(instance_path)
        self.node_file = f"{instance_path}/{NODE_DIRECTORY_FILE}" 
        self.node_directory = util.read_dict_from_file(self.node_file) if os.path.exists(self.node_file) else {}
        self.challenges = {}

    def add_node(self, node):
        self.node_directory[node.checkpoint] = self.get_node_info(node)

    def add_next_n_nodes(self, source, node_info_list):
        for node_info in node_info_list:
            node_info['source'] = source
            self.node_directory[str(node_info['checkpoint'])] = node_info
        self.persist()

    def add_checkpoint(self, node_list, base_checkpoint):
        for i, node in enumerate(sorted(node_list, key=lambda x: f"{x.host}:{x.port}")):
            node.checkpoint = base_checkpoint + i + 1
            self.add_node(node)

    def generate_hash(self, checkpoint_int):
        current_node = self.node_directory[str(checkpoint_int)]
        previous_node = self.node_directory[str(checkpoint_int-1)] if checkpoint_int > 1 else None
        previous_hash = previous_node['hash'] if previous_node != None else DEFAULT_HASH
        return util.generate_hash(self.generate_hashable_string(current_node, previous_hash))

    def generate_hashable_string(self, current_node, previous_hash):
        return f"{current_node['checkpoint']}|{current_node['public_key']}|{current_node['host']}|{current_node['port']}|{previous_hash}"
  
    def generate_hashes(self):
        for i in range(len(self.node_directory)):
            self.set_hash_value(i+1, self.generate_hash(i+1))

    def generate_random_up_to_n_checkpoints(self, n):
         
        if n >= len(self.node_directory):
            # Return all
            print(f"Return all checkpoints")
            return [(i+1) for i in range(len(self.node_directory))]
        else:
            # randomly select n
            print(f"Randomly pick n items")
            return random.sample(range(1,len(self.node_directory)+1),n)

    def get_challenge_id(self, checkpoints):
        challenge_id = len(self.challenges) + 1
        self.challenges[str(challenge_id)] = checkpoints
        return challenge_id

    def get_hash(self, checkpoint):
        if (node_info := self.node_directory.get(str(checkpoint),None)) != None:
            return node_info.get("hash", "no hash")          
        else:
            return f"Node not found for checkpoint: {checkpoint}"

    def get_hashes_for_challenges(self, checkpoint_list):
        return [(checkpoint,self.get_hash(checkpoint)) for checkpoint in checkpoint_list]
        
    def get_host_and_port(self, identifier):
        node_info = self.node_directory[str(identifier)]
        return (node_info['host'], node_info['port'])
            
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

    def size(self):
        return len(self.node_directory)

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

    def set_hash_value(self, checkpoint, hash):
        node_info = self.node_directory[str(checkpoint)] 
        node_info['hash'] = hash

    def set_node_info(self, node):
        if self.has_checkpoint(node.checkpoint):
            entry = self.node_directory.get(node.checkpoint)
            node.status = entry.status
