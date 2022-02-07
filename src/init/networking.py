import asyncio
import command
from handle_challenge import HandleChallenge
from handle_request import HandleRequest
from handle_response import HandleResponse
from listener import Listener
from request import Request
import util

class Networking:

    def __init__(self, node):
        self.node = node
        self.handle_request = HandleRequest(self)
        self.handle_response = HandleResponse(self)
        self.handle_challenge = HandleChallenge(self)
        self.SPINOZA_COIN_PREFIX: Final = b'\x02\x03\x05\x07'
        self.SPINOZA_COIN_SUFFIX: Final = b'\x07\x07\x07\x07'
        self.PREFIX_SIZE: Final = len(self.SPINOZA_COIN_PREFIX)
        self.SUFFIX_SIZE: Final = len(self.SPINOZA_COIN_SUFFIX)

    async def announce_to(self, destination_host, destination_port):
        request = Request(
            networking=self,
            identifier = self.node.get_public_key_value(),
            action_json = { 
                "action_type": command.ANNOUNCE_NODE,
                "host": self.node.host,
                "port": self.node.port
            }
        )
        return await request.send_to(destination_host, destination_port)

    async def broadcast_to(self, broadcast, broadcast_context, iteration_sequence_id, subrange_size, max_parts):
        if (invalid_reason := broadcast.check_if_invalid(self.node)) != None:
           print("broadcast received is invalid: {result} skipping...")
           return False
           
        # add broadcast to the current node
        self.node.add_broadcast(broadcast.get_identifier(), broadcast, broadcast_context)
        if broadcast_context.get_subrange_size() == 1:
            # No more broadcasts are needed.  Nothing needs to be verified
            # return receipt which is a signed json of the broadcast
            return broadcast.get_receipt(self.node)

        subrange_size -= 1
        num_parts = min(max_parts, subrange_size) 
        avg_size_per_part = subrange_size // num_parts
        diff = subrange_size - avg_size_per_parts*num_parts
        iteration_sequence_id = iteration_sequence_id+1
        
        for i in range(1,num_parts+1):
            extra_part = 1 if diff > 0 else 0 
            diff -= extra_part
            destination_host, destination_port = self.node.directory.get_host_and_port(broadcast_context.get_node_id_from_iterator_sequence_id(iteration_sequence_id))

            request = Request(
                networking=self,
                identifier=self.node.checkpoint,
                action_json = {
                    "action_type": command.BROADCAST,
                    "broadcast": broadcast,
                    "broadcast_context": broadcast_context,
                    "iteration_sequence_id": iteration_sequence_id,
                    "subrange_size": avg_size_per_part + extra_part,
                    "max_parts": num_parts
                }
            )
            await request.send_to(destination_host, destination_port)
            
            iteration_sequence_id += avg_size_per_part + extra_part
        # return receipt
        return broadcast.get_receipt(self.node)

    async def check_hash_with(self, destination_host, destination_port, checkpoint, hash):
        print(f"check_hash_with: destination_host: {destination_host}, destination_port: {destination_port}, checkpoint: {checkpoint}, hash: {hash}")
        request = Request(
            networking=self,
            identifier = self.node.checkpoint if self.node.checkpoint != None else self.node.get_public_key_value(),
            action_json = {
                "action_type": command.CHECK_HASH,
                "checkpoint": checkpoint,
                "hash": hash
            }
        )
        return await request.send_to(destination_host, destination_port)

    async def nominate_nodes(self, identifier):
        self.node.close_nominations()
        self.node.directory.add_candidate_to_nominations(identifier)
        start = self.node.checkpoint
        size = self.node.directory.get_number_of_nodes()
        step = util.random_step(size)
        # save signed initiator  -- so that node can trust 
        # randomly iterate through n nodes
        # check if already updated when nominate matches nominate. Use a hash.
        volume = 1
        n = self.node.config.get_num_nodes_returned_per_request()
        if volume == size:
            try:
                print(f"networking: nominate_nodes: volume: {volume} = size: {size}, starting validation")
                asyncio.create_task(self.validate_nominations(self.node.directory.nominee_count()))
            except Exception as e:
                print(f"exception hit in nominate_nodes: {e}")
        else:
            print(f"networking: nominate_nodes: proceed...")
            current_nominations = self.node.directory.get_current_nominations()
            for i in [i for i in range(n) if volume+i+1 < size]:
                self.gossip_nominations(start, step, volume + 1, n, current_nominations)
                
    async def ready_to_join(self, destination_host, destination_port):
        result = None
        try:
            request = Request(
                networking=self,
                identifier = self.node.get_public_key_value(),
                action_json = {
                    "action_type": command.READY_TO_JOIN,
                    "host": self.node.host,
                    "port": self.node.port
                }
            )
            print(f"\nnetworking ready_to_join: destination_host: {destination_host}, destination_port: {destination_port}")
            print(f"request: {request.message.get_encoded_payload()}")
            result=await request.send_to(destination_host, destination_port)
        except Exception as e:
            print(f"Exception hit: {e}")
        return result

    async def resolve_source_inconsistency(self):
        print(f"networking: resolve source inconsistency")

    async def uptake_checkpoints(self):
        print(f"networking: uptake checkpoints")

    async def validate_nominations(self, nominee_count):
        print(f"\nvalidate_nominations: nominee_count: {nominee_count}")
        if self.node.directory.nominee_count() == nominee_count:
            try:
                print(f"Proceeding with validation...")
                self.node.directory.promote_nominations()
                size = self.node.directory.get_number_of_nodes()
                step = util.random_step(size)
                # iterate through n items
                print(f"Iterate through n items")
            except Exception as e:
                print(f"validate_nominations: hit exception: {e}")
        else:
            print(f"Discrepancy found: nominees found: {self.node.directory.nominee_count()}")

    def get_identifier(self):
        return self.node.checkpoint

    async def listen(self):
        print(f"\nlisten: port: {self.node.port}")
        listener = Listener(self)
        return await listener.run() 
