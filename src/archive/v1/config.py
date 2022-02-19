from typing import Final
import os
import util

# Default values
DEFAULT_NUM_NODES_RETURNED_PER_REQUEST: Final = 50

# Fields of config file
INSTANCE_BASE_PATH : Final = "instance_base_path"
HOST : Final = "host"
BASE_PORT : Final = "base_port"
TRUSTED_NODE : Final = "trusted_node"
TRUSTED_PORT : Final = "trusted_port"
COUNT_INSTANCES : Final = "count_instances"
COUNT_DEAD_INSTANCES : Final = "count_dead_instances"
COUNT_UNRELIABLE_INSTANCES : Final = "count_unreliable_instances"
NUM_NODES_RETURNED_PER_REQUEST: Final = "num_nodes_returned_per_request"
LOGGING_LEVEL : Final = "logging_level"

requiredFields = ( 
    INSTANCE_BASE_PATH, 
    HOST, 
    BASE_PORT, 
    TRUSTED_NODE, 
    TRUSTED_PORT, 
    COUNT_INSTANCES, 
    COUNT_DEAD_INSTANCES,
    COUNT_UNRELIABLE_INSTANCES,
    LOGGING_LEVEL 
)

class Config:

    def __init__(self, yaml_file):
        self.config = util.read_yaml(yaml_file)
        self.validate_config(self.config)
        
    def validate_config(self, config):
        for property in requiredFields:
            if property not in config:
                print(f"A required property in the configuration file is missing: {property}")
                exit()
        if NUM_NODES_RETURNED_PER_REQUEST in config and int(config[NUM_NODES_RETURNED_PER_REQUEST]) < DEFAULT_NUM_NODES_RETURNED_PER_REQUEST:
            print(f"{NUM_NODES_RETURNED_PER_REQUEST} must be at least 50")

    def get_instance_base_path(self):
        return os.path.expanduser(self.config[INSTANCE_BASE_PATH])

    def get_host(self):
        return self.config[HOST]

    def get_base_port(self):
        return self.config[BASE_PORT]

    def get_trusted_node(self):
        return self.config[TRUSTED_NODE]
 
    def get_trusted_port(self):
        return self.config[TRUSTED_PORT]

    def get_count_instances(self):
        return self.config[COUNT_INSTANCES]

    def get_count_dead_instances(self):
        return self.config[COUNT_DEAD_INSTANCES]

    def get_count_unreliable_instances(self):
        return self.config[COUNT_UNRELIABLE_INSTANCES]

    def get_num_nodes_returned_per_request(self):
        return int(self.config.get(NUM_NODES_RETURNED_PER_REQUEST, DEFAULT_NUM_NODES_RETURNED_PER_REQUEST))

    def get_logging_level(self):
        return self.config[LOGGING_LEVEL]
