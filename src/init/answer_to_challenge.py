from message import Message
import util

class AnswerToChallenge:

    def __init__(self, reader, writer, networking, identifier, payload_json):
        self.reader = reader
        self.writer = writer
        answer_json = {
            "timestamp": util.utc_timestamp(),
            "answer": payload_json
        } 
        self.message = Message(networking, identifier, answer_json)

    def evaluate(self):
        try:
            print(f"\nAnswerToChallenge: evaluate: message: {self.message.get_encoded_payload()}")
            self.writer.write(self.message.get_encoded_payload())
        except Exception as e:
            print(f"evaluate failed with exception: {e}")
