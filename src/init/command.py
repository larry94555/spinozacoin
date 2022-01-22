from typing import Final

# Commands
#
# 1. ANNOUNCE_NODE: send out host/port/public_key, receive a temporary alias, checkpoint, and list of 100 nodes
ANNOUNCE_NODE: Final = "announce_node"
# 2. UPTAKE_CHECKPOINT: visit each of 100 nodes, send checkpoint and offset, retreive next 100 nodes
UPTAKE_CHECKPOINT: Final = "uptake_checkpoint"
# 3. NODE_DOWN: associate alias with a 'down' status 
NODE_DOWN: Final = "node_down"
# 4. NODE_UNRELIABLE: associate alias with an 'unreliable' status
NODE_UNRELIABLE: Final = "node_unreliable"
# 5. READY_TO_JOIN: a node that has completed the uptake can send this out to any node and must respond to a random 100 nodes.  In return, this triggers the nomination process.
READY_TO_JOIN: Final = "ready_to_join"
# 6. NOMINATE_CHECKPOINT: Each node that receives either NOMINATE_CHECKPOINT or READY_TO_JOIN, send out a NOMINATE_CHECKPOINT in response.  This message keeps track of initiating offset, checkpoint, list of nodes, size
NOMINATE_CHECKPOINT: Final = "nominate_checkpoint"
# 7. VALIDATE_CHECKPOINT: Once a node receives a NOMINATE_NODE where size = size, then the node proceeds to VALIDATE_CHECKPOINT which includes offset, checkpoint, size
VALIDATE_CHECKPOINT: Final = "validate_checkpoint"
