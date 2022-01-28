import asyncio
import command

class HandleResponse:

    def __init__(self, networking):
        self.networking = networking

    async def run(self, response_json):

        print(f"\nHandleResponse.run: response_json: {response_json}")

        response_handler = {
            command.ANNOUNCE_NODE: self.handle_announce_node_response,
            command.UPTAKE_CHECKPOINTS: self.handle_uptake_checkpoints_response,
            command.NODE_DOWN: self.handle_node_down_response,
            command.NODE_UNRELIABLE: self.handle_node_unreliable_response,
            command.READY_TO_JOIN: self.handle_ready_to_join_response,
            command.NOMINATE_CHECKPOINTS: self.handle_nominate_checkpoints_response,
            command.VALIDATE_CHECKPOINTS: self.handle_validate_checkpoints_response,
            command.NODE_UPDATE: self.handle_node_update_response
        }
        action = response_json['body']['response']['action_type']
        return await response_handler[action](response_json)

    # 1. Add nodes received with source included (validate source)
    # 2. If complete, then generate hash and validate with trusted node
    # 3. If all goes well, then send out ready_to_join
    # 4. If all does not go well, identify problem source, add source to list of untrusted, continue update from where left off
    # 5. If not complete, then send out request to next node on list and repeat with step 1.
    async def handle_announce_node_response(self, response_json):
        print(f"\nhandle_announce_node_response: {response_json}")
        source=response_json['identifier']
        response=response_json['body']['response']
        
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
            print(f"do uptake_checkpoint for next n nodes")
        else:
            # validate against trusted node
            # Need to break this up into future actions to not break asynchio
            self.networking.node.directory.generate_hashes()

            # set future action to validate hash
            print(f"\nport: {self.networking.node.port}: check_hash_with trusted node: checkpoint={total_nodes}, hash={self.networking.node.directory.get_hash(total_nodes)}")
            source_host, source_port = self.networking.node.directory.get_host_and_port(identifier)
            print(f"\nsource_host: {source_host}, source_port: {source_port}")
            task = asyncio.create_task(self.networking.check_hash_with(source_host,source_port,checkpoint=total_nodes,hash=(self.networking.node.directory.get_hash(total_nodes))))
            try:
                await asyncio.wait_for(task, timeout=2)
            except asnycio.TimeoutError:
                print("timeout error")
                pass
            
        # if validation successful, do ready_to_join
        # if validation is not successful, identify the flawed source, and get n through update_checkpoint through alternative source
        # if validation is not successful and there are no alternative sources, return saying that the network is down, check with spinozacoin.org for details on when it will be back up
        

    async def handle_uptake_checkpoints_response(self, response_json):
        pass
   
    async def handle_node_down_response(self, response_json):
        pass

    async def handle_node_unreliable_response(self, response_json):
        pass

    async def handle_ready_to_join_response(self, response_json):
        pass

    async def handle_nominate_checkpoints_response(self, response_json):
        pass

    async def handle_validate_checkpoints_response(self, response_json):
        pass

    async def handle_node_update_response(self, response_json):
        pass
