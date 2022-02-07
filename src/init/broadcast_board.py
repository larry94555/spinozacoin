from typing import Final
from iteration_plan import IterationPlan
import util

class BroadcastBoard:

    def __init__(self, instance_path):
        if not os.path.exists(instance_path):
            util.create_directory_if_needed(instance_path)
        self.broadcast_board = {}

    def add_broadcast(self, identifier, broadcast):
        self.broadcast_board[identifier] = broadcast
        

            

     
            
            
           
    

