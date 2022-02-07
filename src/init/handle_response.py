import asyncio
from challenge_answer import ChallengeAnswer
import command
import node

class HandleResponse:

    def __init__(self, networking):
        self.networking = networking

    async def run(self, response_json, transport):
 
        print(f"\nHandleResponse.run: response_json: {response_json}")

        response_handler = {
            command.ANNOUNCE_NODE: self.handle_announce_node_response,
            command.UPTAKE_CHECKPOINTS: self.handle_uptake_checkpoints_response,
            command.NODE_DOWN: self.handle_node_down_response,
            command.NODE_UNRELIABLE: self.handle_node_unreliable_response,
            command.READY_TO_JOIN: self.handle_ready_to_join_response,
            command.NOMINATE_CHECKPOINTS: self.handle_nominate_checkpoints_response,
            command.VALIDATE_CHECKPOINTS: self.handle_validate_checkpoints_response,
            command.NODE_UP: self.handle_node_up_response,
            command.CHECK_HASH: self.handle_check_hash_response,
            command.COMPROMISED: self.handle_compromised_response,
            command.SEND_CHALLENGE_RESULT: self.handle_send_challenge_result_response,
            command.BROADCAST: self.handle_broadcast_response
        }
        try:
            response = response_json['body']['response']
            action_type = response['action_type']
            await response_handler[action_type](response_json, transport, response)
        except Exception as e:
            print(f"HandleResponse: run: hit exception: {e}")

    # 1. Add nodes received with source included (validate source)
    # 2. If complete, then generate hash and validate with trusted node
    # 3. If all goes well, then send out ready_to_join
    # 4. If all does not go well, identify problem source, add source to list of untrusted, continue update from where left off
    # 5. If not complete, then send out request to next node on list and repeat with step 1.
    async def handle_announce_node_response(self, response_json, transport, response):
        print(f"\nhandle_announce_node_response: {response_json}")
        source=response_json['identifier']
        
        #Add values returned to node_directory
        total_nodes = response['checkpoint']
        start = response['start']
        step = response['step']
        identifier = response_json['identifier']
        next_n_nodes = response['next_n_nodes']
        self.networking.node.directory.add_next_n_nodes(source, next_n_nodes)

        print(f"\ndirectory: {self.networking.node.directory.node_directory}")

        if self.networking.node.directory.size() < total_nodes:
            # not done: get next_n_nodes # uptake_checkpoint until complete
            print(f"do uptake_checkpoints for next n nodes")
            asyncio.create_task(self.networking.uptake_checkpoints())
        else:
            # validate against trusted node
            # Need to break this up into future actions to not break asynchio
            self.networking.node.directory.generate_hashes()

            print(f"\nport: {self.networking.node.port}: check_hash_with trusted node: checkpoint={total_nodes}, hash={self.networking.node.directory.get_hash(total_nodes)}")
            source_host, source_port = self.networking.node.directory.get_host_and_port(identifier)
            print(f"\nsource_host: {source_host}, source_port: {source_port}")
            asyncio.create_task(self.networking.check_hash_with(source_host,source_port,checkpoint=total_nodes,hash=(self.networking.node.directory.get_hash(total_nodes))))
            
        # if validation successful, do ready_to_join
        # if validation is not successful, identify the flawed source, and get n through update_checkpoint through alternative source
        # if validation is not successful and there are no alternative sources, return saying that the network is down, check with spinozacoin.org for details on when it will be back up
        

    async def handle_uptake_checkpoints_response(self, response_json, transport, response):
        pass
   
    async def handle_node_down_response(self, response_json, transport, response):
        pass

    async def handle_node_unreliable_response(self, response_json, transport, response):
        pass

    async def handle_ready_to_join_response(self, response_json, transport, response):
        print(f"\nhandle_ready_to_join_response: {response_json}")
        response = response_json['body']['response']
        challenge_id = response['challenge_id']
        checkpoint_list = response['checkpoint_list'] 
        result=self.networking.node.directory.get_hashes_for_challenges(checkpoint_list)
        payload_json = {
            "action_type": command.READY_TO_JOIN,
            "challenge_id": challenge_id,
            "answer": result
        }
        challenge_answer = ChallengeAnswer(
            transport = transport,
            networking = self.networking,
            identifier = self.networking.node.get_public_key_value(),
            payload_json = payload_json
        )
        challenge_answer.send()

    async def handle_nominate_checkpoints_response(self, response_json, transport, response):
        pass

    async def handle_validate_checkpoints_response(self, response_json, transport, response):
        pass

    async def handle_node_up_response(self, response_json, transport, response):
        pass

    async def handle_check_hash_response(self, response_json, transport, response):
        print(f"\nhandle_check_hash_response: {response_json}")
        result = response['result']
        checkpoint = response_json['body']['response']['checkpoint']
        print(f"result: {result}, node status: {self.networking.node.status}, checkpoint: {checkpoint}")
        if self.networking.node.status == node.STATUS_NEW and result == "GOOD":
            self.networking.node.status = node.STATUS_DOWN
            print(f"\nhandle_check_hash_response: node status: {self.networking.node.status}, ready_to_join")
            asyncio.create_task(self.networking.ready_to_join(self.networking.node.config.get_trusted_node(), self.networking.node.config.get_trusted_port()))
        else:
            print(f"\nhandle_check_hash_response: node status: {self.networking.node.status}, result: {result}")
            if self.networking.node.status == node.STATUS_NEW:
                asyncio.create_task(self.networking.resolve_source_inconsistency())
        #return (checkpoint, result)

    async def handle_compromised_response(self, response_json, transport, response):
        pass
        
    async def handle_send_challenge_result_response(self, response_json, transport, response):
        print(f"\nhandle_send_challenge_result")

    async def handle_broadcast_response(self, response_json, transport, response):
        print(f"\nhandle_broadcast_response: response_json: {response_json}")
        
