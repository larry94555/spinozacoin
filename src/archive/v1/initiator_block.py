from typing import Final
import json
import util

BROADCAST_EXPIRATION_IN_SECONDS: Final = 3600

class InitiatorBlock:

    def __init__(self, node_id, message, broadcast_id, timestamp, signature):
        self.__initiator_node_id = node_id
        self.__message = message
        self.__timestamp = timestamp
        self.__initiator_broadcast_id = broadcast_id
        self.__signature = signature

    def check_if_invalid(self, public_key, broadcasts):
        if self.has_expired():
            return "broadcast expired"
        elif self.get_identifier() in broadcasts:
            return "broadcast already received"
        check_signature = util.validate_signature(
            public_key = public_key,
            signature = self.__signature,
            json_string = json.dumps(self.get_initiator_block())
        )
        if not check_signature:
            return "invalid signature"
        else:
            return None

    def get_initiator_block(self):
        return {
            "initiator_node_id": self.__initiator_node_id,
            "message": self.__message,
            "timestamp": self.__timestamp,
            "initiatorbroadcast_id": self.__initiator_broadcast_id
        }

    def get_signature(self):
        return self.__signature

    def set_signature(self, signature):
        self.__signature = signature

    def has_expired(self):
        return util.is_earlier_than(self.__timestamp, util.seconds_ago(BROADCAST_EXPIRATION_IN_SECONDS))

