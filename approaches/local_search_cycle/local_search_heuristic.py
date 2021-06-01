import numpy as np
import random
import operator
import time
from itertools import combinations, product

from approaches.local_search_cycle import cycle_operations
from approaches.abstract_approach import AbstractApproach
from api.replacement import Replacement

class LocalSearch(AbstractApproach):

    def __init__(self, instance):
        self.instance = instance
        self.examples_num_first = np.ceil(instance.matrix.shape[0] / 2)
        self.examples_num_second = instance.matrix.shape[0] - self.examples_num_first
        self.algorithm = 'Local Search'
        self.neighborhood = 'nodes'
        self._first_solution = None
        self._second_solution = None
    
    
    def solve(self, method = 'steepest'):
        if self._first_solution is not None and self._second_solution is not None:
            if method == 'steepest':
                return self._steepest_solution(method)[0]
            elif method == 'greedy':
                return self._greedy_solution(method)[0]
        else:
            print(f'Ustaw wartości cykli.')

    def _greedy_solution(self, method):
        check_first = True
        check_second = True
        total_best_cost = self.compute_total_cost()
        order = ['intraclass', 'interclass']
        
        start = time.time()

        while check_first or check_second:
            #random.seed(42)
            random.shuffle(order)

            for key in order:
                if check_first and key == 'intraclass':
                    local_results = list()
                    local_results += self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._first_solution, computation_cycle=self._second_solution, method=method)
                    if local_results:
                        min_replacement = min(local_results, key=operator.attrgetter('score'))
                        self._first_solution, self._second_solution = min_replacement.first_cycle, min_replacement.second_cycle
                        total_best_cost = min_replacement.score
                        #check_second = True
                    else:
                        check_first = False
            
                if check_second and key == 'intraclass':
                    local_results = list()
                    local_results += self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._second_solution, computation_cycle=self._first_solution, method=method)
                    if local_results:
                        min_replacement = min(local_results, key=operator.attrgetter('score'))
                        self._second_solution, self._first_solution = min_replacement.first_cycle, min_replacement.second_cycle
                        total_best_cost = min_replacement.score
                        #check_first = True
                    else:
                        check_second = False   

                if key == 'interclass':
                    local_results = list()     
                    local_results += self._interclass_computation(best_cost=total_best_cost, method=method)
                    if local_results:
                        min_replacement = min(local_results, key=operator.attrgetter('score'))
                        self._first_solution, self._second_solution = min_replacement.first_cycle, min_replacement.second_cycle
                        total_best_cost = min_replacement.score
                        check_first = True
                        check_second = True
                    else:
                        check_first = False
                        check_second = False 
        return time.time() - start, total_best_cost


    def _steepest_solution(self, method, max_time = float('inf'), total_best_cost = None):
        check_first = True
        check_second = True
        if total_best_cost is None:
            total_best_cost = self.compute_total_cost()
        else:
            total_best_cost = total_best_cost
        
        start = time.time()

        while (check_first or check_second) and (time.time() - start < max_time):

            if check_first:
                local_results = list()
                local_results += self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._first_solution, computation_cycle=self._second_solution, method=method)
                local_results += self._interclass_computation(best_cost=total_best_cost, method=method)
                if local_results:
                    min_replacement = min(local_results, key=operator.attrgetter('score'))
                    self._first_solution, self._second_solution = min_replacement.first_cycle, min_replacement.second_cycle
                    total_best_cost = min_replacement.score
                    check_second = True
                else:
                    check_first = False
            
            if check_second:
                local_results = list()
                local_results += self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._second_solution, computation_cycle=self._first_solution, method=method)
                local_results += self._interclass_computation(best_cost=total_best_cost, method=method, replace=True)
                if local_results:
                    min_replacement = min(local_results, key=operator.attrgetter('score'))
                    self._second_solution, self._first_solution = min_replacement.first_cycle, min_replacement.second_cycle
                    total_best_cost = min_replacement.score
                    check_first = True
                else:
                    check_second = False   
        return time.time() - start, total_best_cost
        

    def _intraclass_computation(self, best_cost, checked_cycle, computation_cycle, method):
        result = list()
        nodes_combination = list(combinations(checked_cycle[:-1], r = 2))
        if method == 'greedy':
            random.shuffle(nodes_combination)

        for (node1, node2) in nodes_combination:
            if self.neighborhood == 'nodes':
                temp_solution, temp_cost = cycle_operations.replace_nodes_inside_cycle(self, node1, node2, checked_cycle[:], best_cost)
                if temp_cost < best_cost:   
                    result.append( Replacement(temp_solution, computation_cycle, temp_cost) )
                    if method == 'greedy':
                        break

            if self.neighborhood == 'edges':
                temp_solution, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node1, node2, checked_cycle[:], best_cost)
                if temp_cost < best_cost: 
                    result.append( Replacement(temp_solution, computation_cycle, temp_cost) )
                    if method == 'greedy':
                        break
        
        return result

    def _interclass_computation(self, best_cost, method, replace = False):
        result = list()

        nodes_product = list(product(self._first_solution[:-1], self._second_solution[:-1]))
        if method == 'greedy':
            random.shuffle(nodes_product)

        for (node1, node2) in nodes_product:
            temp_first_solution, temp_second_solution, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
            if temp_cost < best_cost:   
                if replace:
                    result.append( Replacement(temp_second_solution, temp_first_solution, temp_cost) )
                else:
                    result.append( Replacement(temp_first_solution, temp_second_solution, temp_cost) )
                if method == 'greedy':
                    break
        return result


