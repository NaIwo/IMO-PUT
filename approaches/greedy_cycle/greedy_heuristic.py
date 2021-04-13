import numpy as np
import operator
import time

from approaches.abstract_approach import AbstractApproach
from api.instance import Instance
from api.insertion import Insertion

class Greedy(AbstractApproach):

    def __init__(self, instance, regret = 1, neighbour = False):
        self.instance = instance
        self.regret = regret
        self.examples_num_first = np.ceil(instance.matrix.shape[0] / 2)
        self.examples_num_second = instance.matrix.shape[0] - self.examples_num_first
        self.neighbour = neighbour
        if neighbour:
            self.algorithm = f'Nearest Neighbour'
            self.regret = 0
        else:
            self.algorithm = f'Greedy Cycle'
        self._first_solution = list()
        self._second_solution = list()
    
    
    def solve(self, first_start_node, second_start_node):
        start = time.time()
        self._first_solution, self._second_solution = self._find_solution(first_start_node, second_start_node)
        end = time.time()
        return end - start

    def _find_solution(self, first_start_node, second_start_node):
        first_cycle = [first_start_node, first_start_node] #z ostatniego można przejśc do pierwszego więc dodajemy obydwa w celach imitacji cyklu
        second_cycle = [second_start_node, second_start_node] #z ostatniego można przejśc do pierwszego więc dodajemy obydwa w celach imitacji cyklu

        while len(set(first_cycle)) < self.examples_num_first or len(set(second_cycle)) < self.examples_num_second:
            if len(set(first_cycle)) < self.examples_num_first:
                nodes_not_in_cycle = list(set(range(self.instance.matrix.shape[0])) - set(first_cycle) - set(second_cycle))
                first_cycle = self._find_current_insertion(first_cycle, nodes_not_in_cycle)

            if len(set(second_cycle)) < self.examples_num_second:
                nodes_not_in_cycle = list(set(range(self.instance.matrix.shape[0])) - set(first_cycle) - set(second_cycle))
                second_cycle = self._find_current_insertion(second_cycle, nodes_not_in_cycle)

        return first_cycle, second_cycle

    def _find_current_insertion(self, cycle, nodes_not_in_cycle):
        matrix_cost = dict()
        for idx, node_idx in enumerate(nodes_not_in_cycle):
            local_insertion = list()

            for edge_idx1 in range((self.neighbour * (len(cycle) - 2)), len(cycle) - 1):
                edge_idx2 = edge_idx1 + 1
                ins_cost = self._compute_insertion_cost(node_idx = node_idx, edge_idx1 = cycle[edge_idx1], edge_idx2 = cycle[edge_idx2])
                local_insertion.append(Insertion(node_idx, ins_cost, edge_idx1))

            matrix_cost[idx] = self._sort_insertion(local_insertion)
            
        v_best = self._find_best_insertion(matrix_cost)
        self._insert_into_cycle(cycle, v_best)
        return cycle


    def _sort_insertion(self, local_insertion):
        return sorted(local_insertion, key=operator.attrgetter('insertion_cost', 'node_to_insert'))

    def _compute_insertion_cost(self, node_idx, edge_idx1, edge_idx2):
        temp = self.instance.matrix[edge_idx1, node_idx] + self.instance.matrix[node_idx, edge_idx2]
        return temp - self.instance.matrix[edge_idx1, edge_idx2]

    def _find_best_insertion(self, matrix_cost):
        v_best = None
        regret_result = list()
        for idx, v_cost in matrix_cost.items():
            if self.regret != 0 and len(v_cost) >= 2:
                temp_cost = 0
                range_border = min(self.regret + 1, len(v_cost))
                for i in range(1, range_border):
                    temp_cost += (v_cost[i].insertion_cost - v_cost[0].insertion_cost)
                regret_result.append(temp_cost)

            else:
                regret_result.append(v_cost[0].insertion_cost)

        v_best = self._get_best_node(regret_result)
        return min(matrix_cost[v_best], key=operator.attrgetter('insertion_cost'))
    
    def _insert_into_cycle(self, cycle, v_best):
        index = v_best.place_in_cyce + 1
        value = v_best.node_to_insert
        return cycle.insert(index, value)

    def _get_best_node(self, regret_result):
        if self.regret != 0:
            return np.argmax(regret_result)
        else:
            return np.argmin(regret_result)


