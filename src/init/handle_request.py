import command
from typing import Final
import util

NUM_NODES_RETURNED: Final = 100

class HandleRequest:

    def __init__(self, networking):
        self.networking = networking


    def get_response(self, request_json):

        print(f"\nHandleRequest: get_response: request_json: {request_json}", flush=True)

        command_handler = {
            command.ANNOUNCE_NODE: self.handle_announce_node,
            command.UPTAKE_CHECKPOINTS: self.handle_uptake_checkpoints,
            command.NODE_DOWN: self.handle_node_down,
            command.NODE_UNRELIABLE: self.handle_node_unreliable,
            command.READY_TO_JOIN: self.handle_ready_to_join,
            command.NOMINATE_CHECKPOINTS: self.handle_nominate_checkpoints,
            command.VALIDATE_CHECKPOINTS: self.handle_validate_checkpoints,
            command.NODE_UPDATE: self.handle_node_update,
            command.CHECK_HASH: self.handle_check_hash
        }

        # need to change, json/json seems wrong....
        action = request_json['body']['action']['action_type']
        return command_handler[action](request_json)

    # Returns:
    # 1. checkpoint
    # 2. offset
    # 3. step
    def handle_announce_node(self, request_json):
        print(f"handle_announce_node: request_json: {request_json}", flush=True)
        latest_checkpoint = self.networking.node.directory.size()
        start_pos = util.random_position(latest_checkpoint)
        step = util.random_step(latest_checkpoint)
        return {
            "action_type": command.ANNOUNCE_NODE,
            "checkpoint": latest_checkpoint,
            "start": start_pos,
            "step": step,
            "next_n_nodes": self.networking.node.directory.up_to_n(NUM_NODES_RETURNED, start_pos, step, 0, latest_checkpoint)
        }

    def handle_uptake_checkpoints(self, request_json):
        pass

    def handle_node_down(self, request_json):
        pass

    def handle_node_unreliable(self, request_json):
        pass

    def handle_ready_to_join(self, request_json):
        pass
    
    def handle_nominate_checkpoints(self, request_json):
        pass

    def handle_validate_checkpoints(self, request_json):
        pass

    def handle_node_update(self, request_json):
        pass

    def handle_check_hash(self, request_json):
        print(f"\nhandle_request: handle_check_hash: request_json: {request_json}")
        action = request_json['body']['action'] 
        checkpoint = action['checkpoint']
        if 'hash' not in self.networking.node.directory.node_directory[str(checkpoint)]:
            self.networking.node.directory.generate_hashes()
        hash = self.networking.node.directory.get_hash(checkpoint)
        result = "GOOD" if hash == action['hash'] else "BAD"
        return {
            "action_type": command.CHECK_HASH,
            "checkpoint": checkpoint,
            "hash": action['hash'],
            "result": result
        }
     
