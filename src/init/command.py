from typing import Final

# Commands
#
# 1. ANNOUNCE: send out host/port and receive an alias (starts gossip process to accept a new node)
ANNOUNCE: Final = "announce"
# 2. NODE_UP: associate alias with host, port, timestamp, sequence_id
NEW_NODE: Final = "node_up"
# 3. NODE_DOWN: associate alias with a 'down' status 
NODE_DOWN: Final = "node_down"
# 4. NODE_UNRELIABLE: associate alias with an 'unreliable' status
NODE_UNRELIABLE: Final = "node_unreliable"
# 5. GOSSIP: Spread a message to all nodes
GOSSIP: Final = "gossip"
# 6. RECOGNIZE: recognize that a node is valid

# The open problem is to be able to determine when a node has been validated by all valid nodes.
