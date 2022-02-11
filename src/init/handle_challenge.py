import asyncio
import command
import json
import node_directory
import util

class HandleChallenge:

    def __init__(self, networking):
        self.networking = networking

    def get_result(self, challenge_result_json):
        
        print(f"\nHandleChallenge: instance {self.networking.node.instance_id} get_result: challenge_result_json: {challenge_result_json}")

        command_handler = {
            command.READY_TO_JOIN: self.handle_ready_to_join_challenge
        }
        action = challenge_result_json['body']['challenge_answer']['action_type']
        return command_handler[action](challenge_result_json)

    def handle_ready_to_join_challenge(self, result_json):
        challenge_answer_json = result_json['body']['challenge_answer']
        challenge_id = int(challenge_answer_json['challenge_id'])
        answer = challenge_answer_json['answer']
        response="error"
        result = self.networking.node.directory.validate_hashes(
            challenge_id = challenge_id,
            answer = answer
        )
        if result == node_directory.RESULT_GOOD:
            print(f"\nHandleChallenge: handle_ready_to_join_challenge: instance {self.networking.node.instance_id} Starting the nomination process to assign checkpoint to new node...")
            try:
                receipt_json = {
                    "authorized_action": command.NOMINATE_CHECKPOINTS,
                    "receipt_timestamp": util.utc_timestamp(),
                    "receipt_node_id": self.networking.node.checkpoint,
                    "authorized_node_identifier": result_json['identifier']
                }
                print(f"\nreceipt_json: {receipt_json}")
                proof_of_receipt = util.get_signature_for_json(
                    private_key = self.networking.node.get_private_key(),
                    json_string = json.dumps(receipt_json)
                )
                print(f"\nproof_of_receipt: {proof_of_receipt}")
                response = {
                    "result": result,
                    "proof_of_receipt": proof_of_receipt.hex(),
                    "receipt_json": receipt_json
                }
            except Exception as e:
                print(f"\nhandle_challenge.handle_ready_to_join_challenge: hit error: {e}")
        else:
            print(f"\nHandleChallenge: handle_ready_to_join_challenge: instance {self.networking.node.instance_id} failed ready_to_join")
            response = result
        return {
            "action_type": command.SEND_CHALLENGE_RESULT,
            "challenge_type":  command.READY_TO_JOIN,
            "challenge_result": response
        }
