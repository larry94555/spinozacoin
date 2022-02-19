# broadcast context
#
# The purpose of this class is to manage the broadcast which is sent to all nodes in random order
# 
# The goal is to be efficient (minimize redundancy) and to be reliable (ensure each node receives)
#
# It cannot be assumped that all nodes are up or that all nodes can be trusted
#
# It can be assumed that the initiator can be trusted
#
# In each broadcast, there are 2 roles:  broadcasters (that push the message to up to n nodes and save receipts from each receiver), a validator (a leaf that validates the number of nodes traversed -- number of broadcasters)
#
# Open question: can leafs be used to validate?  A broadcast saves all receipts and nodes that were down and gets the OK from all nodes visited.  A leaf gets the history (nodes that proceeded) and does a skip level.
#
# If the skip-level works, then the broadcast would then forward the skip-level to either the initiator or to another skip level and so on... That's potentially n^2 - n = n(n-1) nodes to each skip level
#
# To Do:  Need to think more about the validator idea to find a way to make it work

class BroadcastContext:

    def __init__(self, size, start, step):
        self.__size = size
        self.__start = start
        self.__step = step
        self.__visits = 0

    def get_node_id_from_iterator_sequence_id(self, i):
        return (self.__start + (i*self.__step)) % self.__size + 1

    def increase_count(self):
        self.__vistits += 1
    
    
