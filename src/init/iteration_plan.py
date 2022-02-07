

# Iteration does the following
# Problem 1: Solve for step=1
# Divide up
# How to divide up a size of s over n.  10/1 -> 1, 10 --> 1 [10]
# 10/2 -> 1,6 --> 1 [5], 1+(10/2) [5]
# 10/3 -> 1,5,8 -> 1 [4], 5 [3], 8 [3]
# 10/4 -> 1,4,7,9 -> 1[3], 4[3], 7[2], 9[2]
# 10/5 -> 1,3,5,7,9 -> 1[2], 3[2], 5[2], 7[2], 9[2]
# 10/6 -> 1,3,5,7,9,10 -> 1[2], 3[2], 5[2], 7[2], 9[1], 10[1]
# 10/7 -> 1,3,5,7,8,9,10 -> 1[2], 3[2], 5[2], 7[1], 8[1], 9[1], 10[1]
# 10/8 -> 1,3,5,6,7,8,9,10 -> 1[2], 3[2], 5[1], 6,[1], 7[1], 8[1], 9[1], 10[1]
# 10/9 -> 1,3,4,5,6,7,8,9,10 ->
class IterationPlan:

    def __init__(self, delta, size, volume, step, n):
        self.delta = delta
        self.size = size
        self.volume = volume
        self.step = step
        self.n = min(n,delta)

    def get_checkpoint(self, i):
        return self.start + (self.volume + i)*self.step % size

    def next_n_nodes(self):
        return range(self.n)

    def divide_size_into_n(self, n, size):
        return [

    def get_plan(i):
        pass


    
