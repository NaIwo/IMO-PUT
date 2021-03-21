import numpy as np
import random
import operator
import time
from itertools import combinations, product

from approaches.abstract_approach import AbstractApproach
from api.replacement import Replacement

class RandomLocalSearch(AbstractApproach):

    def __init__(self, instance):
        self.instance = instance
        self.examples_num_first = np.ceil(instance.matrix.shape[0] / 2)
        self.examples_num_second = instance.matrix.shape[0] - self.examples_num_first
        self.algorithm = 'Random Local Search'
        self._first_solution = None
        self._second_solution = None
    
    
    def solve(self, computation_time):
        if self._first_solution is not None and self._second_solution is not None:
            self._find_solution(computation_time)
        else:
            print(f'Ustaw wartości cykli.')

    def _find_solution(self, computation_time):
        check_first = True
        check_second = True
        total_best_cost = self.compute_total_cost()

        start = time.time()

        while time.time() - start < computation_time:
            method = random.choice([0, 1, 2])
            if method == 0:
                self._first_solution, self._second_solution = self._replace_nodes_between_cycles(random.choice(self._first_solution), \
                                                    random.choice(self._second_solution), \
                                                    self._first_solution, self._second_solution)
            if method == 1:
                cycle = random.choice([0, 1])
                if cycle == 0:
                    self._first_solution = self._replace_nodes_inside_cycle(random.choice(self._first_solution), random.choice(self._first_solution),  self._first_solution)
                else:
                    self._second_solution = self._replace_nodes_inside_cycle(random.choice(self._second_solution), random.choice(self._second_solution),  self._second_solution)
            if method == 2:
                cycle = random.choice([0, 1])
                if cycle == 0:
                    self._first_solution = self._replace_edges_inside_cycle(random.choice(self._first_solution), random.choice(self._first_solution),  self._first_solution)
                else:
                    self._second_solution = self._replace_edges_inside_cycle(random.choice(self._second_solution), random.choice(self._second_solution),  self._second_solution)


    def _replace_nodes_between_cycles(self, first_cycle_node, second_cycle_node, first_cycle, second_cycle):
        first_index = first_cycle.index(first_cycle_node)
        second_index = second_cycle.index(second_cycle_node)

        first_cycle[first_index] = second_cycle_node
        second_cycle[second_index] = first_cycle_node

        first_cycle[-1] = first_cycle[0]
        second_cycle[-1] = second_cycle[0]

        return first_cycle, second_cycle

    def _replace_nodes_inside_cycle(self, first_node, second_node, cycle):
        first_index = cycle.index(first_node)
        second_index = cycle.index(second_node)

        cycle[first_index], cycle[second_index] = second_node, first_node
        cycle[-1] = cycle[0]

        return cycle

    def _replace_edges_inside_cycle(self, first_node, second_node, cycle):
        first_index = cycle.index(first_node) 
        second_index = cycle.index(second_node) 
        part_of_cycle = cycle[first_index:second_index]
        part_of_cycle = part_of_cycle[::-1]
        cycle = cycle[:first_index] + part_of_cycle + cycle[second_index:]
        cycle[-1] = cycle[0]
        return cycle



    


