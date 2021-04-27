import time 
import random

from approaches.local_search_cycle import cycle_operations
from api.replacement import Replacement
from approaches.local_search_cycle.ls_candidates_moves import LocalSearchCandidateMoves
from approaches.greedy_cycle.greedy_heuristic import Greedy

class LocalSearchIterated(LocalSearchCandidateMoves):
    def solve_ils1(self, n_candidats = 8, num_moves = 12, max_time = 10):
        if self._first_solution is not None and self._second_solution is not None:
            return self._ils1_fn(n_candidats, num_moves, max_time)
        else:
            print(f'Ustaw wartości cykli.')

    def solve_ils2(self, n_candidats = 8, num_nodes = 12, max_time = 10, ils2a = True):
        if self._first_solution is not None and self._second_solution is not None:
            return self._ils2_fn(n_candidats, num_nodes, max_time, ils2a)
        else:
            print(f'Ustaw wartości cykli.')

    def _ils1_fn(self, n_candidats, num_moves, max_time):
        cost = self.compute_total_cost()
        solutions_list = list()

        start = time.time()
        _, cost = self._steepest_solution(n_candidats, max_time = max_time - (time.time() - start), total_best_cost = cost)
        solutions_list.append( Replacement(self._first_solution, self._second_solution, cost) )

        while time.time() - start < max_time:
            nodes_f = random.sample(self._first_solution[:-1], k = num_moves+1)
            nodes_s = random.sample(self._second_solution[:-1], k = num_moves+1)
            for i in range(num_moves):
                self._first_solution, cost = cycle_operations.replace_nodes_inside_cycle(self, nodes_f[i], nodes_f[i+1], self._first_solution[:], cost)
                self._second_solution, cost = cycle_operations.replace_nodes_inside_cycle(self, nodes_s[i], nodes_s[i+1], self._second_solution[:], cost)

            nodes_f = random.sample(self._first_solution[:-1], k = num_moves)
            nodes_s = random.sample(self._second_solution[:-1], k = num_moves)
            for i in range(num_moves):
                self._first_solution, self._second_solution, cost = cycle_operations.replace_nodes_between_cycles(self, nodes_f[i], nodes_s[i], self._first_solution[:], self._second_solution[:], cost)

            _, cost = self._steepest_solution(n_candidats, max_time = max_time - (time.time() - start), total_best_cost = cost)
            solutions_list.append( Replacement(self._first_solution, self._second_solution, cost) )
        
        min_sol = min(solutions_list)
        self._first_solution, self._second_solution = min_sol.first_cycle, min_sol.second_cycle
        return time.time() - start

    def _ils2_fn(self, n_candidats, num_nodes, max_time, ils2a):
        cost = self.compute_total_cost()
        solutions_list = list()

        greedy_cycle = Greedy(self.instance, regret = 0)
        start = time.time()
        _, cost = self._steepest_solution(n_candidats, max_time = max_time - (time.time() - start), total_best_cost = cost)
        solutions_list.append( Replacement(self._first_solution, self._second_solution, cost) )

        while time.time() - start < max_time:

            random_perturbation = random.sample(range(int(self.examples_num_first)), k = int(self.examples_num_first * num_nodes/100))
            fs = list(map(self._first_solution.__getitem__, random_perturbation))
            ss = list(map(self._second_solution.__getitem__, random_perturbation))
            fs.append( fs[0] )
            ss.append( ss[0] )

            greedy_cycle.first_solution = fs
            greedy_cycle.second_solution = ss
            _ = greedy_cycle.solve(fs[0], ss[0])

            self._first_solution = greedy_cycle.first_solution
            self._second_solution = greedy_cycle.second_solution

            cost = greedy_cycle.compute_total_cost()
            if ils2a:
                _, cost = self._steepest_solution(n_candidats, max_time = max_time - (time.time() - start), total_best_cost = cost)

            solutions_list.append( Replacement(self._first_solution, self._second_solution, cost) )
        
        min_sol = min(solutions_list)
        self._first_solution, self._second_solution = min_sol.first_cycle, min_sol.second_cycle
        return time.time() - start