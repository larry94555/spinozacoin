import asyncio
import command
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
        result = self.networking.node.directory.validate_hashes(
            challenge_id = challenge_id,
            answer = answer
        )
        if result == node_directory.RESULT_GOOD:
            print(f"\nHandleChallenge: handle_ready_to_join_challenge: instance {self.networking.node.instance_id} Starting the nomination process to assign checkpoint to new node...")
            identifier = result_json['identifier']
            node_info = self.networking.node.directory.get_node_candidate_info(identifier)
            print(f"\nHandleChallenge: handle_ready_to_join_challenge: instance {self.networking.node.instance_id} nominate_nodes: node_info: {node_info}")

            asyncio.create_task(self.networking.nominate_nodes(identifier))
        else:
            print(f"\nHandleChallenge: handle_ready_to_join_challenge: instance {self.networking.node.instance_id} failed ready_to_join")
        return {
            "action_type": command.SEND_CHALLENGE_RESULT,
            "response": result
        }
