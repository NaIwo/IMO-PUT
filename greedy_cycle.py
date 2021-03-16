import numpy as np
import random
import sys

from utils.utils import plot_result
from api.instance import Instance
from approaches.greedy_cycle.greedy_heuristic import Greedy


def read_input(num):
    try:
        name = sys.argv[num]
    except IndexError:
        raise IndexError
    return int(name)

def get_value():
    try:
        regret = read_input(1)
    except IndexError:
        regret = 1
        print(f'Nie podano wartości żalu. Domyślnie: {1}')
    try:
        times = read_input(2)
    except IndexError:
        times = 1
        print(f'Nie podano ilości eksperymentów. Domyślnie: {1}')
    
    return regret, times

def main():
    regret, times = get_value()

    for instance_name in ['kroA100', 'kroB100']:
        instance = Instance(name = instance_name)
        instance.compute_matrix()
        
        #start_node = random.randrange(instance.matrix.shape[0])

        list_of_solutions = list()
        best_greedy = None

        node_to_choose = list(range(instance.matrix.shape[0]))
        for i in range(times):
            start_node = random.choice(node_to_choose)
            node_to_choose = list( set(node_to_choose) - set([start_node]) )

            greedy = Greedy(instance = instance, regret = regret)
            greedy.solve(start_node)

            list_of_solutions.append(greedy.compute_cost())
            if best_greedy is None or list_of_solutions[-1] < best_greedy.compute_cost():
                best_greedy = greedy


        print(f'Instance: {instance_name}')
        print(f'Best Path: {best_greedy.solution}')
        print(f'Best Cost: {best_greedy.compute_cost()}')
        print(f'Min Cost: {min(list_of_solutions)}')
        print(f'Max Cost: {max(list_of_solutions)}')
        print(f'Average Cost: {np.mean(list_of_solutions)}')
        print()

        plot_title = f'{best_greedy.algorithm}, {best_greedy.instance.instance_name}, Regret: {best_greedy.regret}, Distance: {best_greedy.compute_cost()}'
        save_name = '{}-r_{}'.format(best_greedy.instance.instance_name, best_greedy.regret)
        plot_result(best_greedy, plot_title, save_name)
        

if __name__ == "__main__":
    main()