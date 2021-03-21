import random
import numpy as np

class AbstractApproach():
    
    @property
    def first_solution(self):
        return self._first_solution
    
    @first_solution.setter
    def first_solution(self, first_solution):
        self._first_solution = first_solution
    
    @property
    def second_solution(self):
        return self._second_solution
    
    @second_solution.setter
    def second_solution(self, second_solution):
        self._second_solution = second_solution

    def solve(self, first_start_node, second_start_node):
        raise NotImplementedError
    

    def compute_total_cost(self):
        first_cost = 0
        second_cost = 0
        for idx in range(len(self._first_solution) - 1):
            first_cost += self.instance.matrix[self._first_solution[idx], self._first_solution[idx+1]]

        for idx in range(len(self._second_solution) - 1):
            second_cost += self.instance.matrix[self._second_solution[idx], self._second_solution[idx+1]]
        return first_cost + second_cost
    