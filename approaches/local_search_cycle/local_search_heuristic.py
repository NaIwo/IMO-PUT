import numpy as np
import random
import operator
import time
from itertools import combinations, product

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
            return self._find_solution(method)
        else:
            print(f'Ustaw wartości cykli.')

    def _find_solution(self, method):
        check_first = True
        check_second = True
        total_best_cost = self.compute_total_cost()
        order = ['intraclass', 'interclass']
        
        start = time.time()

        while check_first or check_second:
            if method == 'greedy':
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
        return time.time() - start
        


    def _intraclass_computation(self, best_cost, checked_cycle, computation_cycle, method):
        result = list()
        for (node1, node2) in combinations(checked_cycle[:-1], r = 2):
            if self.neighborhood == 'nodes':
                temp_solution, temp_cost = self._replace_nodes_inside_cycle(node1, node2, checked_cycle[:], best_cost)
                if temp_cost < best_cost:   
                    result.append( Replacement(temp_solution, computation_cycle, temp_cost) )
                    if method == 'greedy':
                        break

            if self.neighborhood == 'edges':
                temp_solution, temp_cost = self._replace_edges_inside_cycle(node1, node2, checked_cycle[:], best_cost)
                if temp_cost < best_cost: 
                    result.append( Replacement(temp_solution, computation_cycle, temp_cost) )
                    if method == 'greedy':
                        break
        
        return result

    def _interclass_computation(self, best_cost, method):
        result = list()
        for (node1, node2) in product(self._first_solution[:-1], self._second_solution[:-1]):
            temp_first_solution, temp_second_solution, temp_cost = self._replace_nodes_between_cycles(node1, node2, self._first_solution[:], self._second_solution[:], best_cost)
            if temp_cost < best_cost:   
                result.append( Replacement(temp_first_solution, temp_second_solution, temp_cost) )
                if method == 'greedy':
                    break
        return result

    def _greedy_local_search(self):
        check_first = True
        check_second = True
        total_best_cost = self.compute_total_cost()

        while check_first or check_second:
            if check_first:
                self._first_solution, total_best_cost, check_first = self._intraclass_computation(total_best_cost, self._first_solution, self._second_solution)
            interclass_output, total_best_cost = self._interclass_computation(total_best_cost)
            check_first = check_first or interclass_output

            if check_second:
                self._second_solution, total_best_cost, check_second = self._intraclass_computation(total_best_cost, self._second_solution, self._first_solution)
            interclass_output, total_best_cost = self._interclass_computation(total_best_cost)
            check_second = check_second or interclass_output


    def _replace_nodes_between_cycles(self, first_cycle_node, second_cycle_node, first_cycle, second_cycle, currenct_cost):
        first_index = first_cycle.index(first_cycle_node)
        second_index = second_cycle.index(second_cycle_node)

        c1 = first_cycle[:-1]
        c2 = second_cycle[:-1]
        length1 = len(c1)
        length2 = len(c2)
        new_cost = currenct_cost - (self.instance.matrix[c1[first_index-1], c1[first_index]] +\
                                    self.instance.matrix[c1[first_index], c1[(first_index+1) % length1]] +\
                                    self.instance.matrix[c2[second_index-1], c2[second_index]] +\
                                    self.instance.matrix[c2[second_index], c2[(second_index+1) % length2]]) +\
                                    (self.instance.matrix[c1[first_index-1], c2[second_index]] +\
                                    self.instance.matrix[c2[second_index], c1[(first_index+1) % length1]] +\
                                    self.instance.matrix[c2[second_index-1], c1[first_index]] +\
                                    self.instance.matrix[c1[first_index], c2[(second_index+1) % length2]])
        
        first_cycle[first_index] = second_cycle_node
        second_cycle[second_index] = first_cycle_node

        first_cycle[-1] = first_cycle[0]
        second_cycle[-1] = second_cycle[0]

        return first_cycle, second_cycle, new_cost

    def _replace_nodes_inside_cycle(self, first_node, second_node, cycle, currenct_cost):
        first_index = cycle.index(first_node)
        second_index = cycle.index(second_node)
        c = cycle[:-1]
        length = len(c)
        if first_index == 0 and second_index == length-1:
            new_cost = currenct_cost - (self.instance.matrix[c[second_index-1], c[second_index]] + \
                                        self.instance.matrix[c[first_index], c[(first_index+1) % length]]) + \
                                        (self.instance.matrix[c[second_index-1], c[first_index]] + \
                                        self.instance.matrix[c[second_index], c[(first_index+1) % length]])
        elif second_index - first_index == 1:
            new_cost = currenct_cost - (self.instance.matrix[c[first_index-1], c[first_index]] + \
                                        self.instance.matrix[c[second_index], c[(second_index+1) % length]]) + \
                                        (self.instance.matrix[c[first_index-1], c[second_index]] + \
                                        self.instance.matrix[c[first_index], c[(second_index+1) % length]])
        else:
            new_cost = currenct_cost - (self.instance.matrix[c[first_index-1], c[first_index]] + \
                                    self.instance.matrix[c[first_index], c[(first_index+1) % length]] + \
                                    self.instance.matrix[c[second_index-1], c[second_index]] + \
                                    self.instance.matrix[c[second_index], c[(second_index+1) % length]]) + \
                                    (self.instance.matrix[c[first_index-1], c[second_index]] + \
                                    self.instance.matrix[c[second_index], c[(first_index+1) % length]] + \
                                    self.instance.matrix[c[second_index-1], c[first_index]] + \
                                    self.instance.matrix[c[first_index], c[(second_index+1) % length]])

        cycle[first_index], cycle[second_index] = second_node, first_node
        cycle[-1] = cycle[0]

        return cycle, new_cost

    def _replace_edges_inside_cycle(self, first_node, second_node, cycle, currenct_cost):
        first_index = cycle.index(first_node) 
        second_index = cycle.index(second_node) 
        part_of_cycle = cycle[first_index:second_index]
        part_of_cycle = part_of_cycle[::-1]

        c = cycle[:-1]
        new_cost = currenct_cost - (self.instance.matrix[c[first_index-1], c[first_index]] +\
                                    self.instance.matrix[c[second_index-1], c[second_index]] ) +\
                                    (self.instance.matrix[c[first_index-1], c[second_index-1]] +\
                                    self.instance.matrix[c[first_index], c[second_index]] )

        cycle = cycle[:first_index] + part_of_cycle + cycle[second_index:]
        cycle[-1] = cycle[0]
        return cycle, new_cost



    


