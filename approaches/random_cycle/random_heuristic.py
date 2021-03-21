import numpy as np
import random
import operator

from approaches.abstract_approach import AbstractApproach
from api.instance import Instance
from api.insertion import Insertion

class Random(AbstractApproach):

    def __init__(self, instance, seed = None):
        self.instance = instance
        self.seed = seed
        self.examples_num_first = np.ceil(instance.matrix.shape[0] / 2)
        self.examples_num_second = instance.matrix.shape[0] - self.examples_num_first
        self.algorithm = 'Random Cycle'
        self._first_solution = list()
        self._second_solution = list()
    
    
    def solve(self, first_start_node, second_start_node):
        random.seed(self.seed)
        self._first_solution, self._second_solution = self._find_solution(first_start_node, second_start_node)

    def _find_solution(self, first_start_node, second_start_node):
        first_cycle = [first_start_node]
        second_cycle = [second_start_node] 

        while len(set(first_cycle)) < self.examples_num_first or len(set(second_cycle)) < self.examples_num_second:
            if len(set(first_cycle)) < self.examples_num_first:
                nodes_not_in_cycle = list(set(range(self.instance.matrix.shape[0])) - set(first_cycle) - set(second_cycle))
                first_cycle += [random.choice(nodes_not_in_cycle)]

            if len(set(second_cycle)) < self.examples_num_second:
                nodes_not_in_cycle = list(set(range(self.instance.matrix.shape[0])) - set(first_cycle) - set(second_cycle))
                second_cycle += [random.choice(nodes_not_in_cycle)]

        first_cycle += [first_start_node]
        second_cycle += [second_start_node] 
        
        return first_cycle, second_cycle



