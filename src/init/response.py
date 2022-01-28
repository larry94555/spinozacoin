from message import Message
import util

class Response:
    
    def __init__(self, reader, writer, networking, identifier, payload_json):
        self.reader = reader
        self.writer = writer
        timestamp = util.utc_timestamp()
        response_json = {
            "timestamp": timestamp,
            "response": payload_json
        }
        self.message = Message(networking, identifier, response_json)

    def respond(self):
        try:
            print(f"\nResponse: respond: message: {self.message.get_encoded_payload()}")
            self.writer.write(self.message.get_encoded_payload())
        except Exception as e:
            print(f"respond failed with exception: {e}")

    
