import numpy as np
import random
import sys
from collections import defaultdict
from copy import deepcopy


from helpers.helpers import plot_result, save_string_fn
from api.instance import Instance
from api.replacement import Replacement
from approaches.random_cycle.random_heuristic import Random
#from approaches.greedy_cycle.greedy_heuristic import Greedy
#from approaches.local_search_cycle.local_search_heuristic import LocalSearch
from approaches.own_method.own_method_alg import OwnMethod
#from approaches.local_search_cycle.ls_candidates_moves import LocalSearchCandidateMoves
from approaches.greedy_cycle.greedy_heuristic import Greedy

def read_input(num):
    try:
        name = sys.argv[num]
    except IndexError:
        raise IndexError
    return int(name)

def get_value():
    try:
        times = read_input(1)
    except IndexError:
        times = 1
        print(f'Nie podano ilości eksperymentów. Domyślnie: {1}')
    
    return times

def plot_best(instance, key):
    plot_title = f'{instance.algorithm}, {key}, Distance: {instance.compute_total_cost()}'
    save_name = '{}'.format(key)
    plot_result(instance, plot_title, save_name)
        

def main():
    times_number = get_value()

    times = defaultdict(list)
    scores = defaultdict(list)
    
    for instance_name in ['kroA200', 'kroB200']:
        instance = Instance(name = instance_name)
        instance.compute_matrix()

        ####################################
        max_time = 600.0
        print(f'MSLS time: {max_time}')
        for number in range(times_number):
            print(f'Global iteration number: {number+1}')

            ##################################################################
            print('\t-> OwnMethod')
            own_method = OwnMethod(instance)
            own_method.neighborhood = 'edges' 
            own_method.first_solution = None
            own_method.second_solution = None
            time = own_method.solve(max_time = max_time)
            times[f'OwnMethod, {instance_name}'].append(time)
            scores[f'OwnMethod, {instance_name}'].append(deepcopy(own_method))
            print(own_method.compute_total_cost())



        
    save_string = '\n'
    worst_time = float('-inf')
    for key in scores.keys():
        best = min(scores[key], key=lambda el: el.compute_total_cost())
        costs = list( map(lambda el: el.compute_total_cost(), scores[key]) )
        save_string += f'Version: {key}\nMean: {np.mean(costs)}\nMin: {min(costs)}\nMax: {max(costs)}\n\n|TIMES|\n'
        save_string += f'\nMean: {np.mean(times[key])}\nMin: {min(times[key])}\nMax: {max(times[key])}\n\n==========\n\n'
        if np.mean(times[key]) > worst_time:
            worst_time = np.mean(times[key])
        plot_best(best, key)
    
    print(save_string)
    save_string_fn(save_string, 'OwnMethod_results', None)





if __name__ == "__main__":
    main()