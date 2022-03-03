"""
There are 2 types of entries
1. node_id which is str(int)
2. neighborhood_id which is a random number of the form f"N{random id}"
"""


import math
import util

class NodeDirectory:
    """
    Main class for node directory
    """

    NODE_DIRECTORY_FILE = "node_directory.json"
    NODE_COUNT = "node_count"
    NODE_BACKUP_HISTORY = 1

    def __init__(self, instance_path):
        self.node_file = f"{instance_path}/{self.NODE_DIRECTORY_FILE}"
        self.node_db = {}
        self.node_db[self.NODE_COUNT] = 0

    def get_address(self, node_id):
        """
        return address which (host, port)
        """
        host = self.get_node_property(node_id, 'host')
        port = self.get_node_property(node_id, 'port')
        return None if host is None or port is None else (host, port)

    def get_max_id(self):
        """
        return max node id
        """
        return self.node_db[self.NODE_COUNT]

    def get_neighborhood(self, node_id, neighborhood_size):
        """
        return the neighborhood for the given node.
        """
        #print(f"\nget_neighborhood: node_id: {node_id}, size: {neighborhood_size}")
        neighborhood_start = node_id - ((node_id-1) % neighborhood_size)
        #print(f"neighborhood_start: {neighborhood_start}")
        result=[self.node_db[str(i)] for i in range(neighborhood_start,
            neighborhood_start+neighborhood_size) if str(i) in self.node_db]
        return result + [self.node_db[str(i+1)] for i in range(0,
            neighborhood_size - len(result)) if str(i+1) in self.node_db and
                                                self.node_db[str(i+1)] not in result]

    def get_neighborhood_by_limits(self, start_id, last_id):
        """
        return neighborhood based on start_id and last_id
        """
        return [self.node_db[str(i)] for i in range(start_id,last_id+1)]

    def get_node_info(self, node_id):
        """
        return node info based on node_id
        """
        return self.node_db[str(node_id)] if str(node_id) in self.node_db else None

    def get_node_property(self, node_id, node_property):
        """
        return a property of a given node.
        """
        return self.node_db[str(node_id)][node_property] if (
            str(node_id) in self.node_db) else None

    def get_public_key(self, node_id):
        """
        return public key from directory
        """
        return self.get_node_property(node_id, "public_key")

    def has_node_id(self, node_id):
        """
        return true if node id exists in directory
        """
        return str(node_id) in self.node_db

    def persist(self):
        """
        persist directory
        """
        #util.backup_file(self.node_file, self.NODE_BACKUP_HISTORY)
        #util.write_dict_to_file(self.node_db, self.node_file)
        pass

    def populate_bootstraps(self, node_list, neighborhood_size):
        """
        populate directory with test data
        """
        print(f"\nNodeDirectory:populate_bootstraps: nodecount: {len(node_list)}")
        # add node values
        # add neighborhood values
        for i,node in enumerate(node_list):
            node_id = i+1
            self.node_db[str(node_id)] = {
                "node_id": node_id,
                "public_key": node.get_public_key(),
                "host": node.info.host,
                "port": node.info.port,
                "status": node.status.value
            }
        self.node_db[self.NODE_COUNT] = len(node_list)
        # assign values for neighborhoods
        num_neighborhoods = math.ceil(len(node_list)/neighborhood_size)
        print(f"Number of neighborhoods: {num_neighborhoods}")
        self.persist()

    def set_node_info(self, node):
        """
        set node info for a given node
        """
        if self.has_node_id(node.node_id):
            entry = self.db.get(node.node_id)
            node.status = entry.status
