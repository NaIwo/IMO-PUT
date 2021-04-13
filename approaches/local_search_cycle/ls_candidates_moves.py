import numpy as np
import random
import operator
import time
from copy import deepcopy
from itertools import combinations, product

from approaches.local_search_cycle import cycle_operations
from approaches.abstract_approach import AbstractApproach
from api.replacement import Replacement

class LocalSearchCandidateMoves(AbstractApproach):

    def __init__(self, instance):
        self.instance = instance
        self.examples_num_first = np.ceil(instance.matrix.shape[0] / 2)
        self.examples_num_second = instance.matrix.shape[0] - self.examples_num_first
        self.algorithm = 'Local Search Candidate Moves'
        self.neighborhood = 'nodes'
        self._first_solution = None
        self._second_solution = None
    
    
    def solve(self, n_candidats):
        if self._first_solution is not None and self._second_solution is not None:
            return self._steepest_solution(n_candidats)
        else:
            print(f'Ustaw wartości cykli.')


    def _steepest_solution(self, n_candidats):
        check_first = True
        check_second = True
        total_best_cost = self.compute_total_cost()
        
        start = time.time()

        nearest_neighbours = dict()
        for node in range(len(self.instance.matrix)):
            nearest_neighbours[node] = np.argsort(self.instance.matrix[node])[1:n_candidats+1]

        while check_first or check_second:

            if check_first:
                check_first = False
                candidate = list()
                local_best = total_best_cost
                for i, node in enumerate(self._first_solution[:-1]):
                    solutions = self._get_which_solution(node, nearest_neighbours[node])
                    for i_n, neighbour in enumerate(nearest_neighbours[node]):
                        if solutions[neighbour] == 'FIRST':
                            temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node, neighbour, self._first_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [temp_solution[:], self._second_solution[:]]
                            j = i-1
                            if j == -1:
                                j = -2
                            node = self._first_solution[j]
                            j_n = i_n-1
                            if j_n == -1:
                                j_n = -2
                            neighbour = self._first_solution[j_n]
                            temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node, neighbour, self._first_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [temp_solution[:], self._second_solution[:]]
                        else:
                            node2 = self._first_solution[i+1]
                            temp_first_solution, temp_second_solution, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node2, neighbour, self._first_solution[:], self._second_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [temp_first_solution[:], temp_second_solution[:]]

                            j = i-1
                            if j == -1:
                                j = -2
                            node2 = self._first_solution[j]
                            temp_first_solution, temp_second_solution, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node2, neighbour, self._first_solution[:], self._second_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [temp_first_solution[:], temp_second_solution[:]]
                if candidate:
                    check_first = True
                    total_best_cost = local_best
                    self._first_solution = deepcopy(candidate[0])
                    self._second_solution = deepcopy(candidate[1])
                    
           ################################################ 
            if check_second:
                check_second = False
                candidate = list()
                local_best = total_best_cost
                for i, node in enumerate(self._second_solution[:-1]):
                    solutions = self._get_which_solution(node, nearest_neighbours[node])
                    for i_n, neighbour in enumerate(nearest_neighbours[node]):
                        if solutions[neighbour] == 'SECOND':
                            temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node, neighbour, self._second_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [self._first_solution[:], temp_solution[:]]
                            
                            j = i-1
                            if j == -1:
                                j = -2
                            node = self._second_solution[j]
                            j_n = i_n-1
                            if j_n == -1:
                                j_n = -2
                            neighbour = self._second_solution[j_n]
                            temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node, neighbour, self._second_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [self._first_solution[:], temp_solution[:]]
                        else:
                            node2 = self._second_solution[i+1]
                            temp_first_solution, temp_second_solution, temp_cost = cycle_operations.replace_nodes_between_cycles(self, neighbour, node2, self._first_solution[:], self._second_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [temp_first_solution[:], temp_second_solution[:]]

                            j = i-1
                            if j == -1:
                                j = -2
                            node2 = self._second_solution[j]
                            temp_first_solution, temp_second_solution, temp_cost = cycle_operations.replace_nodes_between_cycles(self, neighbour, node2, self._first_solution[:], self._second_solution[:], total_best_cost)
                            if temp_cost < local_best:
                                local_best = temp_cost
                                candidate = [temp_first_solution[:], temp_second_solution[:]]
                if candidate:
                    check_second = True
                    total_best_cost = local_best
                    self._first_solution = deepcopy(candidate[0])
                    self._second_solution = deepcopy(candidate[1])
        return time.time() - start
        
    def _get_which_solution(self, node, sorted_neighbours):
        solutions = dict()
        for n in sorted_neighbours:
            if n in self._first_solution:
                solutions[n] = 'FIRST'
            else:
                solutions[n] = 'SECOND'
        return solutions