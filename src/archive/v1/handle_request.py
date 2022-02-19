import command
import util

class HandleRequest:

    def __init__(self, networking):
        self.networking = networking


    def get_response(self, request_json):

        print(f"\nHandleRequest: instance {self.networking.node.instance_id} get_response: request_json: {request_json}")

        command_handler = {
            command.ANNOUNCE_NODE: self.handle_announce_node,
            command.UPTAKE_CHECKPOINTS: self.handle_uptake_checkpoints,
            command.NODE_DOWN: self.handle_node_down,
            command.NODE_UNRELIABLE: self.handle_node_unreliable,
            command.READY_TO_JOIN: self.handle_ready_to_join,
            command.NOMINATE_CHECKPOINTS: self.handle_nominate_checkpoints,
            command.VALIDATE_CHECKPOINTS: self.handle_validate_checkpoints,
            command.NODE_UP: self.handle_node_up,
            command.CHECK_HASH: self.handle_check_hash,
            command.COMPROMISED: self.handle_compromised,
            command.BROADCAST: self.handle_broadcast
        }

        # need to change, json/json seems wrong....
        action = request_json['body']['action']
        action_type = action['action_type']
        return command_handler[action_type](request_json, action)

    # Returns:
    # 1. checkpoint
    # 2. offset
    # 3. step
    def handle_announce_node(self, request_json, action):
        latest_checkpoint = self.networking.node.directory.size()
        start_pos = util.random_position(latest_checkpoint)
        step = util.random_step(latest_checkpoint)
        num_nodes = self.networking.node.config.get_num_nodes_returned_per_request()
        return {
            "action_type": command.ANNOUNCE_NODE,
            "checkpoint": latest_checkpoint,
            "start": start_pos,
            "step": step,
            "next_n_nodes": self.networking.node.directory.up_to_n(num_nodes, start_pos, step, 0, latest_checkpoint)
        }

    def handle_uptake_checkpoints(self, request_json, action):
        pass

    def handle_node_down(self, request_json, action):
        pass

    def handle_node_unreliable(self, request_json, action):
        pass

    def handle_ready_to_join(self, request_json, action):
        # generate a list of checkpoints to check
        n = self.networking.node.config.get_num_nodes_returned_per_request()
        checkpoints = self.networking.node.directory.generate_random_up_to_n_checkpoints(n)
        self.challenge_id = self.networking.node.directory.get_challenge_id(checkpoints)
        node_info = {
            "public_key": request_json['identifier'],
            "host": action['host'],
            "port": action['port']
        }
        self.networking.node.directory.add_node_candidate(request_json['identifier'], node_info)
        return {
            "action_type": command.READY_TO_JOIN,
            "challenge_id": self.challenge_id,
            "checkpoint_list": checkpoints
        }
    
    def handle_nominate_checkpoints(self, request_json, action):
        pass

    def handle_validate_checkpoints(self, request_json, action):
        pass

    def handle_node_up(self, request_json, action):
        pass

    def handle_check_hash(self, request_json, action):
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

    def handle_compromised(self, request_json, action):
        pass

    def handle_broadcast(self, request_json, action):
        # Forward request 
        receipt=self.networking.broadcast_to(
	    broadcast=action['broadcast'],
            broadcast_context=action['broadcast_context'],
            iteration_sequence_id=action['iteration_sequence_id'],
            subrange_size=action['subrange_size'],
            max_parts=action['max_parts']
        )
        # Sleep 
        # Reach out to confirm with validators
        return {
            "action_type": command.BROADCAST,
            "receipt": receipt
        }
         
