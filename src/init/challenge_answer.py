import util
from message import Message

class ChallengeAnswer:

    def __init__(self, transport, networking, identifier, payload_json):
        self.transport = transport
        challenge_json = {
            "timestamp": util.utc_timestamp(),
            "challenge_answer": payload_json
        } 
        self.message = Message(networking, identifier, challenge_json)
        
    def send(self):
        try:
            print(f"\nchallenge_answer: send: message: {self.message.get_encoded_payload()}") 
            self.transport.write(self.message.get_encoded_payload())
        except Exception as e:
            print(f"challenge_answer failed with exception {e}")
