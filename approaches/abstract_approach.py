import random
import numpy as np

class AbstractApproach():
    
    def __init__(self, instance):
        self.instance = instance
        self.name_with_regret = '{}'.format(instance.instance_name)
        self.examples_num = np.ceil(instance.matrix.shape[0] / 2)
        self.algorithm = 'Random Cycle'
        self._solution = []

    @property
    def solution(self):
        return self._solution

    def solve(self, start_node):
        cycle = [start_node, start_node]
        while len(cycle) - 1 <= self.examples_num:
            matrix_cost = dict()
            nodes_not_in_cycle = list( set(range(self.instance.matrix.shape[0])) - set(cycle) )
            cycle.insert(random.randrange(len(cycle)), random.choice(nodes_not_in_cycle))
        self._solution = cycle
    

    def compute_cost(self):
        cost = 0
        for idx in range(len(self._solution) - 1):
            cost += self.instance.matrix[self._solution[idx], self._solution[idx+1]]
        return cost