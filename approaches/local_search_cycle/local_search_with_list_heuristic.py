import numpy as np
from copy import deepcopy
import random
import time
from sortedcontainers import SortedList
from itertools import combinations, product

from approaches.local_search_cycle import cycle_operations
from approaches.abstract_approach import AbstractApproach
from api.replacement import Replacement

class LocalSearchWithList(AbstractApproach):

    def __init__(self, instance):
        self.instance = instance
        self.examples_num_first = np.ceil(instance.matrix.shape[0] / 2)
        self.examples_num_second = instance.matrix.shape[0] - self.examples_num_first
        self.algorithm = 'Local Search With List'
        self.neighborhood = 'edges'
        self._first_solution = None
        self._second_solution = None
    
    
    def solve(self):
        if self._first_solution is not None and self._second_solution is not None:
            return self._steepest_solution()
        else:
            print(f'Ustaw wartości cykli.')

    def _steepest_solution(self):
        check_first = True
        check_second = True
        total_best_cost = self.compute_total_cost()
        
        start = time.time()

        local_results_first = SortedList()
        local_results_second = SortedList()
        self._init_results_lists(total_best_cost, local_results_first, local_results_second)
        while check_first or check_second:
            if check_first:
                check_first, check_second, operation, candidate, total_best_cost = self._perform_operations(total_best_cost, local_results_first, check_first, check_second, '_first_solution')
                if operation == 2 and candidate is not None:
                    self._get_lists_update_after_interclass(total_best_cost, candidate, local_results_first, local_results_second)
                elif operation == 1 and candidate is not None:
                    self._get_lists_update_after_intraclass(total_best_cost, candidate, local_results_first, '_first_solution')
            ######################################################
            if check_second:
                check_second, check_first, operation, candidate, total_best_cost = self._perform_operations(total_best_cost, local_results_second, check_second, check_first, '_second_solution')
                if operation == 2 and candidate is not None:
                    self._get_lists_update_after_interclass(total_best_cost, candidate, local_results_first, local_results_second)
                elif operation == 1 and candidate is not None:
                    self._get_lists_update_after_intraclass(total_best_cost, candidate, local_results_second, '_second_solution')
        return time.time() - start
        
    def _perform_operations(self, total_best_cost, local_results, check_first, check_second, solution):
        removed_list = list()
        final_candidate = None
        for candidate in local_results:
            operation = self._check_applicable(candidate, solution)
            if operation == 1:
                sol, local_best_cost = cycle_operations.replace_edges_inside_cycle(self, candidate.node1, candidate.node2, getattr(self, solution)[:], total_best_cost)
                if local_best_cost < total_best_cost:
                    setattr(self, solution, sol)
                    total_best_cost = local_best_cost
                    check_second = True
                    removed_list.append(candidate)
                    final_candidate = candidate
                    break
            elif operation == 2:
                fs, ss, local_best_cost \
                                    = cycle_operations.replace_nodes_between_cycles(self, candidate.node1, candidate.node2, self._first_solution[:], self._second_solution[:], total_best_cost)
                if local_best_cost < total_best_cost:
                    self._first_solution, self._second_solution, total_best_cost = fs, ss, local_best_cost
                    check_second = True
                    removed_list.append(candidate)
                    final_candidate = candidate
                    break
            elif operation == -1:
                removed_list.append(candidate)
        for rm in removed_list:
            local_results.remove(rm)
        if final_candidate is None:
            check_first = False
        return check_first, check_second, operation, final_candidate, total_best_cost

    def _init_results_lists(self, total_best_cost, local_results_first, local_results_second):
        self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._first_solution, \
                                                                            computation_cycle=self._second_solution, result=local_results_first)
        self._interclass_computation(best_cost=total_best_cost, result = local_results_first)
        self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._second_solution, \
                                                    computation_cycle=self._first_solution, result=local_results_second, main_cycle='_second_solution')
        self._interclass_computation(best_cost=total_best_cost, result = local_results_second)

    def _get_lists_update_after_interclass(self, total_best_cost, candidate, local_results_first, local_results_second):
        self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._second_solution, \
                                            computation_cycle=None, new_node = candidate.node1, result=local_results_second, main_cycle='_second_solution')
        self._intraclass_computation(best_cost=total_best_cost, checked_cycle=self._first_solution, \
                            computation_cycle=None, new_node = candidate.node2, result=local_results_first)
        self._interclass_computation(best_cost=total_best_cost, new_node1=candidate.node1, new_node2=candidate.node2, result = local_results_first)
        self._interclass_computation(best_cost=total_best_cost, new_node1=candidate.node1, new_node2=candidate.node2, result = local_results_second)
    
    def _get_lists_update_after_intraclass(self, total_best_cost, candidate, local_results, main_cycle = '_second_solution'):
        self._intraclass_computation(best_cost=total_best_cost, checked_cycle=getattr(self, main_cycle), \
                                            computation_cycle=None, new_node = candidate.node2, result=local_results, main_cycle=main_cycle)
        self._intraclass_computation(best_cost=total_best_cost, checked_cycle=getattr(self, main_cycle), \
                            computation_cycle=None, new_node = candidate.node1, result=local_results, main_cycle=main_cycle)

        self._interclass_computation(best_cost=total_best_cost, new_node1=candidate.node1, new_node2=candidate.node2, result = local_results, main_cycle = main_cycle)


    def _intraclass_computation(self, best_cost, checked_cycle, computation_cycle, new_node = None, result = SortedList(), main_cycle = '_first_solution'):
        if new_node is None:
            nodes_product = list(combinations(checked_cycle[:-1], r = 2))
        else:
            nodes_product = list(product([new_node], checked_cycle[:-1]))

        for (node1, node2) in nodes_product:
            _, temp_cost = cycle_operations.replace_edges_inside_cycle(self, node1, node2, checked_cycle[:], best_cost)
            if temp_cost < best_cost: 
                result.add( Replacement(None, None, temp_cost, node1, node2, 'intraclass', main_cycle) )

    def _interclass_computation(self, best_cost, new_node1 = None, new_node2 = None, result = SortedList(), main_cycle = None):
        if new_node1 is None:
            nodes_product = list(product(self._first_solution[:-1], self._second_solution[:-1]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )
        elif main_cycle == '_second_solution':
            nodes_product = list(product(self._first_solution[:-1], [new_node1]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )

            nodes_product = list(product(self._first_solution[:-1], [new_node2]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )
        elif main_cycle == '_first_solution':
            nodes_product = list(product([new_node1], self._second_solution[:-1]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )

            nodes_product = list(product([new_node2], self._second_solution[:-1]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )
        else:
            nodes_product = list(product(self._first_solution[:-1], [new_node1]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )

            nodes_product = list(product([new_node2], self._second_solution[:-1]))
            for (node1, node2) in nodes_product:
                _, _, temp_cost = cycle_operations.replace_nodes_between_cycles(self, node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
                if temp_cost < best_cost:   
                    result.add( Replacement(None, None, temp_cost, node1, node2, 'interclass') )

        


    def _check_applicable(self, candidate, solution):
        if candidate.operation_type == 'intraclass':
            solution = getattr(self, solution)[:-1]
            if candidate.node1 in solution and candidate.node2 in solution:
                if solution.index(candidate.node1) < solution.index(candidate.node2):
                    return 1
                else:
                    return 0
            else:
                return -1
        else: #candidate.operation_type == 'interclass':
            if candidate.node1 in self._first_solution and candidate.node2 in self._second_solution:
                return 2
            else:
                return -1
