from typing import Final
import datetime
import json
import util

# 1. A broadcast is always identified by an initiator (node_id, message, timestamp, broadcast_id, proof-of-initiator) 
#    
#    The initiator block includes a node in the directory (node_id), the message being broadcast (json format), 
#    the timestamp for when it initiated in utc, broadcast_id (a sequence maintained by the node)
#    a proof-of-initiator which is a hash of the intiator block signed by the initiator's private key
#
# 2. A broadcast can be rejected if any of the following are true:
#    
#    * The timestamp has expired
#    * The broadcast_id for that node has already been received
#    * The proof-of-initiator does not match the current public key
#
# 3. A broadcast skips any node that is douwn and that node will need to resync when it comes back up.
# 
#    The process for resyncing is documented in the node directory
#
# 4.  An identifier is what uniquely identifies a broadcast.  This consists of the identifier proof-of-initiator hash
#
# 5.

# For now, setting to 60 minutes
BROADCAST_EXPIRATION_IN_SECONDS: Final = 3600

class Broadcast:
    
    def __init__(self, node, message):
        self.__initiator_node_id = node.checkpoint
        self.__message = message
        self.__timestamp  = util.utc_timestamp()
        self.__initiator_broadcast_id = node.get_next_broadcast_id() 
        self.__proof_of_broadcast = util.get_signature_for_json(
            private_key = node.get_private_key(),
            json_string = json.dumps(self.get_initiator_block()) 
        )

    def build_receipt(self, node):
        receipt_json = {
            "initiator_block": self.get_initiator_block(),
            "receipt_timestamp": util.utc_timestamp(),
            "receipt_node_id": node.get_id()
        }
        proof_of_receipt = util.get_signature_for_json(
            private_key = node.get_private_key(),
            json_string = json.dumps(receipt_json)
        )
        return {
            "receipt_json": receipt_json,
            "proof_of_receipt": proof_of_receipt
        }

    def check_if_invalid(self, node):
        if self.has_expired():
            return "broadcast expired"
        elif self.get_identifier() in node.broadcasts():
            return "broadcast already received"
        check_receipt = util.validate_signature(
                 public_key = node.get_public_key(),
                 signature = self.__proof_of_broadcast,
                 json_string = json.dumps(self.get_initiator_block())
                 )
        if not check_receipt:
            return "invalid signature" 
        else:
            return None

    def get_identifier(self):
        return (self.__initiator_node_id, self.__initiator_broadcast_id)

    def get_initiator_block(self):
        return {
            "initiator_node_id": self.__initiator_node_id,
            "message": self.__message,
            "timestamp": self.__timestamp,
            "initiator_broadcast_id": self.__initiator_broadcast_id
        }

    def get_initiator_broadcast_id(self):
        return self.__initiator_broadcast_id

    def get_initiator_node_id(self):
        return self.__initiator_node_id

    def get_message(self):
        return self.__message

    def get_proof_of_broadcast(self):
        return self.__proof_of_broadcast

    def get_timestamp(self):
        return self.__timestamp

    def has_expired(self):
        return util.is_earlier_than(self.__timestamp, util.seconds_ago(BROADCAST_EXPIRATION_IN_SECONDS))
