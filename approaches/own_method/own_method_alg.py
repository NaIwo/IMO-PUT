import time 
import random
from numpy import argmax
import numpy as np

from approaches.local_search_cycle import cycle_operations
from api.replacement import Replacement
from approaches.local_search_cycle.ls_candidates_moves import LocalSearchCandidateMoves
from approaches.greedy_cycle.greedy_heuristic import Greedy
from approaches.local_search_cycle.local_search_iterated import LocalSearchIterated
from approaches.local_search_cycle.local_search_heuristic import LocalSearch

class OwnMethod(LocalSearch):

    def __init__(self, instance):
        super(OwnMethod, self).__init__(instance)
        self.algorithm = 'Own Method'
        self.solutions = list()

    
    def solve(self, max_time = 10):
        return self._own_method(max_time)

    def _local_local_search(self, solution, max_time):
        ls_candidates_moves = LocalSearchCandidateMoves(self.instance)
        ls_candidates_moves.neighborhood = 'edges' 

        ls_candidates_moves.first_solution = solution.first_cycle[:]
        ls_candidates_moves.second_solution = solution.second_cycle[:]
        _ = ls_candidates_moves.solve(n_candidats = 8)

        solution.first_cycle, solution.second_cycle, solution.score = ls_candidates_moves.first_solution, ls_candidates_moves.second_solution, ls_candidates_moves.compute_total_cost()
        return solution
    
    def _child_in_population(self, child):
        for solution in self.solutions:
            if solution == child:
                return True
        return False

    def _remove_edges(self, cycle, edges):
        edges = set(edges)
        result = []
        for i in range(len(cycle) - 1):
            edge1 = cycle[i]
            edge2 = cycle[i + 1]
            edge3 = cycle[(i + 2) % len(cycle)]
            edge4 = cycle[(i + 3) % len(cycle)]
            if (edge1, edge2) in edges or (edge2, edge1) in edges:
                if edge1 not in result:
                    result.append( edge1 )
                if edge2 not in result:
                    result.append( edge2 )
                continue
            if (edge1, edge3) in edges or (edge3, edge1) in edges:
                if edge1 not in result:
                    result.append( edge1 )
                if edge3 not in result:
                    result.append( edge3 )
                continue
            if (edge1, edge4) in edges or (edge4, edge1) in edges:
                if edge1 not in result:
                    result.append( edge1 )
                if edge3 not in result:
                    result.append( edge4 )
                continue

        return result

    def _recombination(self, parent1, parent2):
        parent2_edges1 = [ (parent2.first_cycle[i], parent2.first_cycle[i+1]) for i in range(len(parent2.first_cycle) - 1) ]
        parent2_edges2 = [ (parent2.second_cycle[i], parent2.second_cycle[i+1]) for i in range(len(parent2.second_cycle) - 1) ]

        result1 = self._remove_edges(parent1.first_cycle[:], parent2_edges1)
        result2 = self._remove_edges(parent1.second_cycle[:], parent2_edges2)
        return result1, result2
    
    def _ero(self, parent, edges):
        K = []
        N = parent[0]
        while len(K) <  len(parent)-1:
            K.append( N )
            in_list = set( K )
            for n in edges[N]:
                if not n in edges.keys():
                    continue
                edges[n] = edges[n] - in_list

            l = float('inf')
            if len(edges[N]) == 0:
                N = random.choice(list(set(parent) - in_list))
            else:
                for n in edges[N]:
                    if not n in edges.keys():
                        continue
                    if len(edges[n]) < l:
                        shortest = []
                        shortest.append( n )
                        l = len(edges[n])
                    elif len(edges[n]) == l:
                        shortest.append( n )
                if len(shortest) == 0:
                    N = random.choice(list(set(parent) - in_list))
                else:
                    N = random.choice(shortest)
        #print(K, len(set(K)))
        return K





    def _recombination3(self, parent1, parent2):
        parent1_edges1 = dict()
        parent1_edges2 = dict()
        parent2_edges1 = dict()
        parent2_edges2 = dict()

        parent1_edges1[parent1.first_cycle[0]] = set((parent1.first_cycle[len(parent1.first_cycle) - 2], parent1.first_cycle[1]))
        parent1_edges2[parent1.second_cycle[0]] = set((parent1.second_cycle[len(parent1.first_cycle) - 2], parent1.second_cycle[1]))
        parent2_edges1[parent2.first_cycle[0]] = set((parent2.first_cycle[len(parent1.first_cycle) - 2], parent2.first_cycle[1]))
        parent2_edges2[parent2.second_cycle[0]] = set((parent2.second_cycle[len(parent1.first_cycle) - 2], parent2.second_cycle[1]))
        for i in range(1, len(parent1.first_cycle) - 1):
            parent1_edges1[parent1.first_cycle[i]] = set((parent1.first_cycle[i-1], parent1.first_cycle[i+1]))
            parent1_edges2[parent1.second_cycle[i]] = set((parent1.second_cycle[i-1], parent1.second_cycle[i+1]))
            parent2_edges1[parent2.first_cycle[i]] = set((parent2.first_cycle[i-1], parent2.first_cycle[i+1]))
            parent2_edges2[parent2.second_cycle[i]] = set((parent2.second_cycle[i-1], parent2.second_cycle[i+1]))

        edges1 = dict()
        edges2 = dict()
        for i in range(len(parent1.first_cycle) - 1):
            edges1[parent2.first_cycle[i]] = parent1_edges1[parent1.first_cycle[i]] | parent2_edges1[parent2.first_cycle[i]]
            edges1[parent1.first_cycle[i]] = parent1_edges1[parent1.first_cycle[i]] | parent2_edges1[parent2.first_cycle[i]]

            edges2[parent2.second_cycle[i]] = parent1_edges2[parent1.second_cycle[i]] | parent2_edges2[parent2.second_cycle[i]]
            edges2[parent1.second_cycle[i]] = parent1_edges2[parent1.second_cycle[i]] | parent2_edges2[parent2.second_cycle[i]]
            
        result1 = self._ero(list(set(parent1.first_cycle[:] + parent2.first_cycle[:])), edges1)
        result2 = self._ero(list(set(parent1.second_cycle[:] + parent2.second_cycle[:])), edges2)
        #print(len(set(list(result1) + list(result2))))
        return result1, result2

    def _recombination2(self, parent1, parent2):
        size = int(self.examples_num_first // 2)
        node = random.choice(list(range(size)))
        result1 = parent1.first_cycle[node:node+size]
        for n in parent2.first_cycle:
            if len(result1) == self.examples_num_first:
                break
            if n not in result1:
                result1.append(n)

        node = random.choice(list(range(size)))
        result2 = parent1.second_cycle[node:node+size]
        for n in parent2.second_cycle:
            if len(result2) == self.examples_num_first:
                break
            if n not in result2:
                result2.append(n)
            
        #print(len(set(list(result1) + list(result2))))
        return result1, result2
            

        
    def _init_population(self):
        unavailable_points = list()
        for i in range(20):
            first_start_node = random.choice( list( set(list(self.instance.point_dict.keys())) - set(unavailable_points) ) )
            second_start_node = np.argmax(self.instance.matrix[first_start_node])
            unavailable_points.append(first_start_node)
            unavailable_points.append(second_start_node)
            #Get random solution
            greedy_cycle = Greedy(self.instance, regret = 0, neighbour = True)
            greedy_cycle.solve(first_start_node, second_start_node)
            population = Replacement(greedy_cycle.first_solution[:], greedy_cycle.second_solution[:], greedy_cycle.compute_total_cost())
            self.solutions.append( population )

    def _add_if_empty(self, fs, ss, node1, node2):
        if len(fs) == 0:
            fs = [node1]
        if len(ss) == 0:
            ss = [node2]
        fs.append( fs[0] )
        ss.append( ss[0] )
        return fs, ss

    def _greedy(self, fs, ss):
        greedy_cycle = Greedy(self.instance, regret = 0)
        greedy_cycle.first_solution = fs
        greedy_cycle.second_solution = ss
        _ = greedy_cycle.solve(fs[0], ss[0])
        return Replacement(greedy_cycle.first_solution[:], greedy_cycle.second_solution[:], greedy_cycle.compute_total_cost())

    def _own_method(self, max_time):

        start = time.time()
        self._init_population()
        for solution in self.solutions:
            solution = self._local_local_search(solution, max_time - (time.time() - start))

        improvement = 0
        while time.time() - start < max_time:
            print(f'\t\t->{time.time() - start}')
            [first_parent, second_parent, third_parent, fourth_parent] = random.sample(self.solutions, k = 4) 
            first_parent_copy_fs = first_parent.first_cycle[:]
            first_parent_copy_ss = first_parent.second_cycle[:]

            #third_parent_copy_fs = third_parent.first_cycle[:]
            #third_parent_copy_ss = third_parent.second_cycle[:]
         
            fs1, ss1 = self._recombination(first_parent, second_parent)
            #fs2, ss2 = self._recombination(third_parent, fourth_parent)

            fs1, ss1 = self._add_if_empty(fs1, ss1, first_parent_copy_fs[0], first_parent_copy_ss[0])
            #fs2, ss2 = self._add_if_empty(fs2, ss2, third_parent_copy_fs[0], third_parent_copy_ss[0])

            parent1 = self._greedy(fs1, ss1)            
            #parent2 = self._greedy(fs2, ss2)  
            
            #if parent1.score < parent2.score:
            #    fs, ss = self._recombination2(parent1, parent2)
            #else:
            #    fs, ss = self._recombination2(parent2, parent1)
            
            #parent = self._greedy(fs, ss)   

            self._first_solution = parent1.first_cycle[:]
            self._second_solution = parent1.second_cycle[:]

            cost = parent1.score

            _, cost = self._steepest_solution(method = 'steepest', max_time = max_time - (time.time() - start), total_best_cost = cost)

            child = Replacement(self._first_solution[:], self._second_solution[:], cost)
            if not self._child_in_population(child):   
                idx = argmax(self.solutions)
                if child.score < self.solutions[idx].score:
                    self.solutions[idx] = child
                    improvement = 0
                else:
                    improvement += 1
                if improvement >= 5:
                    print(f'\t\t\t->Iterated')
                    self.solutions = sorted(self.solutions)
                    for i in range(len(self.solutions)-1, len(self.solutions) - len(self.solutions)//4, -1):
                        local_search = LocalSearchIterated(self.instance)
                        local_search.neighborhood = 'edges' 
                        local_search.first_solution = self.solutions[i].first_cycle[:]
                        local_search.second_solution = self.solutions[i].second_cycle[:]
                        local_search.solve_ils2(n_candidats = 8, num_nodes = 10, max_time = min(max_time - (time.time() - start), 10), ils2a = False)
                        child = Replacement(local_search.first_solution[:], local_search.second_solution[:], local_search.compute_total_cost())
                        if not self._child_in_population(child):   
                            if child.score < self.solutions[i].score:
                                self.solutions[i] = child
                    np.random.shuffle(self.solutions)
                    improvement = 0

        
        min_sol = min(self.solutions)
        self._first_solution, self._second_solution = min_sol.first_cycle, min_sol.second_cycle

        return time.time() - start