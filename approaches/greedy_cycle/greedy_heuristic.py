import numpy as np
import operator

from approaches.abstract_approach import AbstractApproach
from api.instance import Instance
from api.insertion import Insertion

class Greedy(AbstractApproach):

    def __init__(self, instance, regret = 1):
        self.instance = instance
        self.regret = regret
        self.examples_num = np.ceil(instance.matrix.shape[0] / 2)
        self.algorithm = 'Greedy Cycle'
        self._solution = []
    
    @property
    def solution(self):
        return self._solution
    
    def solve(self, start_node):
        self._solution = self._find_solution(start_node)

    def _find_solution(self, start_node):
        cycle = [start_node, start_node] #z ostatniego można przejśc do pierwszego więc dodajemy obydwa w celach imitacji cyklu

        while len(cycle) - 1 <= self.examples_num:
            matrix_cost = dict()
            
            nodes_not_in_cycle = list( set(range(self.instance.matrix.shape[0])) - set(cycle) )
            for idx, node_idx in enumerate(nodes_not_in_cycle):
                local_insertion = list()

                for edge_idx1 in range(len(cycle) - 1):
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


