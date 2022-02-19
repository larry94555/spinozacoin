from message import Message
import util

class ChallengeResult:
    
    def __init__(self, reader, writer, networking, identifier, payload_json):
        self.reader = reader
        self.writer = writer
        challenge_result_json = {
            "timestamp": util.utc_timestamp(),
            "response": payload_json
        }
        self.message = Message(networking, identifier, challenge_result_json)

    def send(self):
        try:
            print(f"\nChallengeResult: send: message: {self.message.get_encoded_payload()}")
            self.writer.write(self.message.get_encoded_payload())
        except Exception as e:
            print(f"send failed with exception: {e}")

