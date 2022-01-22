import json
import util

class Message:

    def __init__(self, networking, identifier, message_json):
        self.networking = networking
        signature = util.get_signature_for_json(
            private_key = networking.node.get_private_key(),
            json_string = json.dumps(message_json)
        )
        self._encoded_payload = self.build_encoded_payload(
            json_string=json.dumps({
                "identifier": identifier,
                "signature": signature.hex(),
                "json": message_json
            })
        )

    def build_encoded_payload(self, json_string):
        return self.networking.SPINOZA_COIN_PREFIX + json_string.encode() + self.networking.SPINOZA_COIN_SUFFIX

    def get_encoded_payload(self):
        return self._encoded_payload

    
