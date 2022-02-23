# There are 2 types of entries
# 1. node_id which is str(int)
# 2. neighborhood_id which is a random number of the form f"N{random id}"

import util

class NodeDirectory:

    NODE_DIRECTORY_FILE = "node_directory.json"
    NODE_BACKUP_HISTORY = 1

    def __init__(self, instance_path):
        self.node_file = f"{instance_path}/{self.NODE_DIRECTORY_FILE}"
        self.db = {}

    def has_node_id(self, node_id):
        return str(node_id) in self.db

    def persist(self):
        util.backup_file(self.node_file, self.NODE_BACKUP_HISTORY)
        util.write_dict_to_file(self.db, self.node_file)
        
    def populate_bootstraps(self, node_list):
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
                "status": node.status
            }
        self.persist()

    def set_node_info(self, node):
        if self.has_node_id(node.node_id):
            entry = self.db.get(node.node_id)
            node.status = entry.status
