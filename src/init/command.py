from typing import Final

# Commands
#
# 1. ANNOUNCE_NODE: send out host/port/public_key, receive a checkpoint and list of up to 100 nodes
# checkpoint is the size
# ANNOUNCE_NODE(host, port, public key) --> (partial node_list [unless less than 100], checkpoint (is the count), offset, step)
ANNOUNCE_NODE: Final = "announce_node"
# 2. UPTAKE_CHECKPOINT: visit each of 100 nodes, send checkpoint start, offset, retreive next n nodes, etc.
# UPTAKE_CHECKPOINT(host, ip, public key, checkpoint, count, offset, step, steps_so_far) -> (partial node_list [unless less than 100 left], checkpoint, count, offset, step)
UPTAKE_CHECKPOINT: Final = "uptake_checkpoint"
# 3. NODE_DOWN: associate alias with a 'down' status, send out a node_down update to 5 nodes (who will then gossip, unless they have already gossiped).  Each node individually checks.  If back up, call out node_down to the node itself.
# NODE_DOWN(identifier, checkpoint, count, offset, step, steps_so_far) -> signed ACK
NODE_DOWN: Final = "node_down"
# 4. NODE_UNRELIABLE: associate alias with an 'unreliable' status
# TBD: THis one needs to evaluated.  node_unreliable is tricky since it can be used to discredit a node in good standing by a bad actor.
NODE_UNRELIABLE: Final = "node_unreliable"
# 5. READY_TO_JOIN: a node that has completed the uptake can send this out to any node and must respond to a random 100 nodes.  In return, this triggers the nomination process.
READY_TO_JOIN: Final = "ready_to_join"
# 6. NOMINATE_CHECKPOINT: Each node that receives either NOMINATE_CHECKPOINT or READY_TO_JOIN, send out a NOMINATE_CHECKPOINT in response.  This message keeps track of initiating offset, checkpoint, list of nodes, size
NOMINATE_CHECKPOINT: Final = "nominate_checkpoint"
# 7. VALIDATE_CHECKPOINT: Once a node receives a NOMINATE_NODE where size = size, then the node proceeds to VALIDATE_CHECKPOINT which includes offset, checkpoint, size
VALIDATE_CHECKPOINT: Final = "validate_checkpoint"
# 8. NODE_UPDATE: either change public alias or come back after being down
NODE_UPDATE: Final = "node_update"
