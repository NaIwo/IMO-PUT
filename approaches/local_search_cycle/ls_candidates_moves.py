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
        self.total_best_cost = None
    
    
    def solve(self, n_candidats):
        if self._first_solution is not None and self._second_solution is not None:
            return self._steepest_solution(n_candidats)
        else:
            print(f'Ustaw wartości cykli.')


    def _steepest_solution(self, n_candidats):
        check_first = True
        check_second = True
        self.total_best_cost = self.compute_total_cost()
        
        start = time.time()

        nearest_neighbours = dict()
        for node in range(len(self.instance.matrix)):
            nearest_neighbours[node] = np.argsort(self.instance.matrix[node])[1:n_candidats+1]
        
        while check_first or check_second:

            if check_first:
                check_first = False
                candidates = list()
                local_best = self.total_best_cost
                for node_idx, node in enumerate(self._first_solution[:-1]):
                    solutions, solutions_idx = self._get_which_solution(node, nearest_neighbours[node])
                    for i_n, neighbour in enumerate(nearest_neighbours[node]):
                        if solutions[neighbour] == 'FIRST':
                            if solutions_idx[neighbour] < node_idx:
                                continue
                            self._perform_inside_cycle('_first_solution', node, node_idx, neighbour, solutions_idx, candidates)
                        else:
                            self._perform_between_cycles('_first_solution', node_idx, neighbour, candidates) 
                if candidates:
                    check_first = True
                    self._save_candidate(min(candidates))
                    
           ################################################ 
            if check_second:
                check_second = False
                candidates = list()
                local_best = self.total_best_cost
                for node_idx, node in enumerate(self._second_solution[:-1]):
                    solutions, solutions_idx = self._get_which_solution(node, nearest_neighbours[node])
                    for i_n, neighbour in enumerate(nearest_neighbours[node]):
                        if solutions[neighbour] == 'SECOND':
                            if solutions_idx[neighbour] < node_idx:
                                continue
                            self._perform_inside_cycle('_second_solution', node, node_idx, neighbour, solutions_idx, candidates)
                        else:
                            self._perform_between_cycles('_second_solution', node_idx, neighbour, candidates) 
                if candidates:
                    check_second = True
                    self._save_candidate(min(candidates))
        return time.time() - start
        
    def _get_which_solution(self, node, sorted_neighbours):
        solutions = dict()
        solutions_idx = dict()
        for n in sorted_neighbours:
            if n in self._first_solution:
                solutions[n] = 'FIRST'
                solutions_idx[n] = self._first_solution.index(n)
            else:
                solutions[n] = 'SECOND'
                solutions_idx[n] = self._second_solution.index(n)
        return solutions, solutions_idx

    def _perform_between_cycles(self, main_solution, node_idx, neighbour, candidates):
        solution = getattr(self, main_solution)[:]
        if candidates:
            local_best = min(candidates).score
        else:
            local_best = self.total_best_cost
        
        if main_solution == '_first_solution':
            temp_first_solution, temp_second_solution, temp_cost \
                                = cycle_operations.replace_nodes_between_cycles(self, solution[node_idx+1], neighbour, \
                                                                                self._first_solution[:], self._second_solution[:], \
                                                                                self.total_best_cost)
        else:
            temp_first_solution, temp_second_solution, temp_cost \
                                = cycle_operations.replace_nodes_between_cycles(self, neighbour, solution[node_idx+1], \
                                                                                self._first_solution[:], self._second_solution[:], \
                                                                                self.total_best_cost)
        if temp_cost < local_best:
            local_best = temp_cost
            candidates.append( Replacement(temp_first_solution[:], temp_second_solution[:], temp_cost) )

        j = node_idx-1
        if j == -1:
            j = -2
        if main_solution == '_first_solution':
            temp_first_solution, temp_second_solution, temp_cost \
                                = cycle_operations.replace_nodes_between_cycles(self, solution[j], neighbour, \
                                                                                self._first_solution[:], self._second_solution[:], \
                                                                                self.total_best_cost)
        else:
            temp_first_solution, temp_second_solution, temp_cost \
                                = cycle_operations.replace_nodes_between_cycles(self, neighbour, solution[j], \
                                                                                self._first_solution[:], self._second_solution[:], \
                                                                                self.total_best_cost)
        if temp_cost < local_best:
            local_best = temp_cost
            candidates.append( Replacement(temp_first_solution[:], temp_second_solution[:], temp_cost) )
    
    def _perform_inside_cycle(self, main_solution, node, node_idx, neighbour, solutions_idx, candidates):
        if candidates:
            local_best = min(candidates).score
        else:
            local_best = self.total_best_cost

        solution = getattr(self, main_solution)[:]
        temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node, neighbour, solution, self.total_best_cost)
        if temp_cost < local_best:
            local_best = temp_cost
            if main_solution == '_first_solution':
                candidates.append( Replacement(temp_solution[:], self._second_solution[:], temp_cost) )
            else:
                candidates.append( Replacement(self._first_solution[:], temp_solution[:], temp_cost) )

        if node_idx+1 == solutions_idx[neighbour]:
            return
        j_n = solutions_idx[neighbour]+1
        if j_n == len(solution)-1:
            return

        temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, solution[node_idx+1], solution[j_n], solution, self.total_best_cost)
        if temp_cost < local_best:
            local_best = temp_cost
            if main_solution == '_first_solution':
                candidates.append( Replacement(temp_solution[:], self._second_solution[:], temp_cost) )
            else:
                candidates.append( Replacement(self._first_solution[:], temp_solution[:], temp_cost) )
    
    def _save_candidate(self, best_candidate):
        self.total_best_cost = best_candidate.score
        self._first_solution = best_candidate._first_cycle
        self._second_solution = best_candidate._second_cycle