# There are 2 types of entries
# 1. node_id which is str(int)
# 2. neighborhood_id which is a random number of the form f"N{random id}"

import math
import util

class NodeDirectory:

    NODE_DIRECTORY_FILE = "node_directory.json"
    NODE_COUNT = "node_count"
    NODE_BACKUP_HISTORY = 1

    def __init__(self, instance_path):
        self.node_file = f"{instance_path}/{self.NODE_DIRECTORY_FILE}"
        self.db = {}
        self.db[self.NODE_COUNT] = 0

    def get_max_id(self):
        return self.db[self.NODE_COUNT]

    def get_neighborhood(self, node_id, neighborhood_size):
        print(f"\nget_neighborhood: node_id: {node_id}, size: {neighborhood_size}")
        neighborhood_start = node_id - ((node_id-1) % neighborhood_size)
        print(f"neighborhood_start: {neighborhood_start}")
        result=[self.db[str(i)] for i in range(neighborhood_start, neighborhood_start+neighborhood_size) if str(i) in self.db]
        return result + [self.db[str(i+1)] for i in range(0, neighborhood_size - len(result)) if str(i+1) in self.db and self.db[str(i+1)] not in result]

    def get_neighborhood_by_limits(self, start_id, last_id):
        return [self.db[str(i)] for i in range(start_id,last_id+1)]

    def has_node_id(self, node_id):
        return str(node_id) in self.db

    def persist(self):
        util.backup_file(self.node_file, self.NODE_BACKUP_HISTORY)
        util.write_dict_to_file(self.db, self.node_file)
        
    def populate_bootstraps(self, node_list, neighborhood_size):
        print(f"NodeDirectory:populate_bootstraps: nodecount: {len(node_list)}")
        # add node values
        # add neighborhood values
        for i,node in enumerate(node_list):
            node_id = i+1
            self.db[str(node_id)] = {
                "node_id": node_id,
                "public_key": node.get_public_key(),
                "host": node.host,
                "port": node.port,
                "status": node.status.value
            }
        self.db[self.NODE_COUNT] = len(node_list)
        # assign values for neighborhoods
        num_neighborhoods = math.ceil(len(node_list)/neighborhood_size)
        self.persist()

    def set_node_info(self, node):
        if self.has_node_id(node.node_id):
            entry = self.db.get(node.node_id)
            node.status = entry.status
