from typing import Final

# Commands
#
# 1. ANNOUNCE_NODE: send out host/port/public_key, receive a checkpoint and list of up to 100 nodes
# checkpoint is the size
# ANNOUNCE_NODE(host, port, public key) --> (partial node_list [unless less than 100], checkpoint (is the count), offset, step)
ANNOUNCE_NODE: Final = "announce_node"
# 2. UPTAKE_CHECKPOINT: visit each of 100 nodes, send checkpoint start, offset, retreive next n nodes, etc.
# UPTAKE_CHECKPOINT(host, ip, public key, checkpoint, count, offset, step, steps_so_far) -> (partial node_list [unless less than 100 left], checkpoint, count, offset, step)
UPTAKE_CHECKPOINTS: Final = "uptake_checkpoints"
# 3. NODE_DOWN: associate alias with a 'down' status, send out a node_down update to 5 nodes (who will then gossip, unless they have already gossiped).  Each node individually checks.  If back up, call out node_down to the node itself.
# NODE_DOWN(identifier, checkpoint, count, offset, step, steps_so_far) -> signed ACK
NODE_DOWN: Final = "node_down"
# 4. NODE_UNRELIABLE: associate alias with an 'unreliable' status
# This is analogous to a node_down.  Call is taken as a heads up where the node proceeds to do a reliability check.
# This is a random 100 checkpoints to verify the hash.  If it is good, then it ignores the call.  If it fails, the node is added to the list of unreliable and it gossips the result to n others.
# A node unreliable or node down is undone by a ready to join or node update
NODE_UNRELIABLE: Final = "node_unreliable"
# 5. READY_TO_JOIN: a node that has completed the uptake can send this out to any node and must respond to a random 100 nodes.  In return, this triggers the nomination process.
READY_TO_JOIN: Final = "ready_to_join"
# 6. NOMINATE_CHECKPOINT: Each node that receives either NOMINATE_CHECKPOINT or READY_TO_JOIN, send out a NOMINATE_CHECKPOINT in response.  This message keeps track of initiating offset, checkpoint, list of nodes, size
NOMINATE_CHECKPOINTS: Final = "nominate_checkpoints"
# 7. VALIDATE_CHECKPOINT: Once a node receives a NOMINATE_NODE where size = size, then the node proceeds to VALIDATE_CHECKPOINT which includes offset, checkpoint, size
VALIDATE_CHECKPOINTS: Final = "validate_checkpoints"
# 8. NODE_UPDATE: either change public alias or come back after being down.  It still needs to go through a validate_checkpoint to be accepted back in.
NODE_UPDATE: Final = "node_update"
# 9. CHECK_HASH: send out a checkpoint and hash to validate it is consistent
# A node send out a checkpoint and a hash.  The node sends back either OK or BAD signed
CHECK_HASH: Final = "check_hash"
# 10.  COMPROMISED: initiate a broadcast that a private key has been compromised
# Can only be sent by a node that has the private key
COMPROMISED: Final = "compromised"
# 11. SEND_CHALLENGE_RESULT: forward result status after a challenge
SEND_CHALLENGE_RESULT: Final = "send_challenge_result"
