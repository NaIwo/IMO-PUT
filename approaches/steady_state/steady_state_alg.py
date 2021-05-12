import time 
import random
from numpy import argmax

from approaches.local_search_cycle import cycle_operations
from api.replacement import Replacement
from approaches.local_search_cycle.ls_candidates_moves import LocalSearchCandidateMoves
from approaches.greedy_cycle.greedy_heuristic import Greedy

class SteadyState(LocalSearchCandidateMoves):

    def __init__(self, instance, solutions):
        super(SteadyState, self).__init__(instance)
        self.algorithm = 'Steady State'
        self.solutions = solutions

    
    def solve(self, n_candidats, max_time = 10, ls = True):
        return self._steady_state(n_candidats, max_time, ls)

    def _local_local_search(self, solution, n_candidats, max_time):
        self.first_solution = solution.first_cycle
        self.second_solution = solution.second_cycle
        _, cost = self._steepest_solution(n_candidats, max_time = max_time, total_best_cost = solution.score)
        solution.first_cycle, solution.second_cycle, solution.score = self._first_solution[:], self._second_solution[:], cost
        self._first_solution, self._second_solution = None, None
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
            if (edge1, edge2) in edges or (edge2, edge1) in edges:
                if edge1 not in result:
                    result.append( edge1 )
                if edge2 not in result:
                    result.append( edge2 )

        return result

    def _recombination(self, parent):
        parent2_edges1 = [ (parent.first_cycle[i], parent.first_cycle[i+1]) for i in range(len(parent.first_cycle) - 1) ]
        parent2_edges2 = [ (parent.second_cycle[i], parent.second_cycle[i+1]) for i in range(len(parent.second_cycle) - 1) ]

        result1 = self._remove_edges(self._first_solution[:], parent2_edges1)
        result2 = self._remove_edges(self._second_solution[:], parent2_edges2)
        return result1, result2
        
            

        

    def _steady_state(self, n_candidats, max_time, ls):
        greedy_cycle = Greedy(self.instance, regret = 0)

        start = time.time()
        for solution in self.solutions:
            solution = self._local_local_search(solution, n_candidats, max_time - (time.time() - start))

        while time.time() - start < max_time:
            [first_parent, second_parent] = random.sample(self.solutions, k = 2) 
            self._first_solution = first_parent.first_cycle[:]
            self._second_solution = first_parent.second_cycle[:]
         
            fs, ss = self._recombination(second_parent)
            if len(fs) == 0:
                fs = [self._first_solution[0]]
            if len(ss) == 0:
                ss = [self._second_solution[0]]

            fs.append( fs[0] )
            ss.append( ss[0] )

            greedy_cycle.first_solution = fs
            greedy_cycle.second_solution = ss
            _ = greedy_cycle.solve(fs[0], ss[0])

            self._first_solution = greedy_cycle.first_solution
            self._second_solution = greedy_cycle.second_solution

            cost = greedy_cycle.compute_total_cost()
            if ls:
                _, cost = self._steepest_solution(n_candidats, max_time = max_time - (time.time() - start), total_best_cost = cost)

            child = Replacement(self.first_solution[:], self.second_solution[:], cost)
            if not self._child_in_population(child):   
                idx = argmax(self.solutions)
                if child.score < self.solutions[idx].score:
                    self.solutions[idx] = child
        
        min_sol = min(self.solutions)
        self._first_solution, self._second_solution = min_sol.first_cycle, min_sol.second_cycle
        return time.time() - start