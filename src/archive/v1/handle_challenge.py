import asyncio
from broadcast import Broadcast
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
                identifier = result_json['identifier']
                node_info = self.networking.node.directory.get_node_candidate_info(identifier)
                broadcast = Broadcast(
                    node=self.networking.node,
                    message = {
                        "action_type": command.NOMINATE_CHECKPOINTS,
                        "public_key": result_json['identifier'].encode().hex(),
                        "host": node_info['host'],
                        "port": node_info['port']
                    }
                )
                proof_of_receipt = util.get_signature_for_json(
                    private_key = self.networking.node.get_private_key(),
                    json_string = json.dumps(broadcast.get_initiator_block())
                )
                response = {
                    "result": result,
                    "proof_of_receipt": proof_of_receipt.hex(),
                    "initiator_block": broadcast.get_initiator_block()
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
