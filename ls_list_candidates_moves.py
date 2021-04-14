import numpy as np
import random
import sys
from collections import defaultdict
from copy import deepcopy

from helpers.helpers import plot_result, save_string_fn
from api.instance import Instance
from approaches.random_cycle.random_heuristic import Random
from approaches.greedy_cycle.greedy_heuristic import Greedy
from approaches.local_search_cycle.local_search_heuristic import LocalSearch
from approaches.local_search_cycle.local_search_with_list_heuristic import LocalSearchWithList
from approaches.local_search_cycle.ls_candidates_moves import LocalSearchCandidateMoves

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

        for number in range(times_number):
            first_start_node = random.choice(list(instance.point_dict.keys()))
            second_start_node = np.argmax(instance.matrix[first_start_node])
            
            print(f'Iteration number: {number+1}')
            #Get random solution
            random_cycle = Random(instance, seed = None)
            random_cycle.solve(first_start_node, second_start_node)
            #plot_random(random_cycle)

            ##################################################################
            #Greedy cycle
            greedy_cycle = Greedy(instance, regret = 0)
            time = greedy_cycle.solve(first_start_node, second_start_node)
            times[f'greedy, regret 0, {instance_name}'].append(time)
            scores[f'greedy, regret 0, {instance_name}'].append(deepcopy(greedy_cycle))

            ##################################################################
            #Local Search
            local_search = LocalSearch(instance)
            local_search.neighborhood = 'edges' 

            #steepest, edges, random
            local_search.first_solution = random_cycle.first_solution[:]
            local_search.second_solution = random_cycle.second_solution[:]
            time = local_search.solve(method = 'steepest')
            times[f'steepest, edges, random, {instance_name}'].append(time)
            scores[f'steepest, edges, random, {instance_name}'].append(deepcopy(local_search))
            
            ##################################################################
            #LocalSearchWithList
            local_search_with_list = LocalSearchWithList(instance)
            local_search_with_list.neighborhood = 'edges' 

            #steepest with LM,, edges, random
            local_search_with_list.first_solution = random_cycle.first_solution[:]
            local_search_with_list.second_solution = random_cycle.second_solution[:]
            time = local_search_with_list.solve()
            times[f'LM, edges, random, {instance_name}'].append(time)
            scores[f'LM, edges, random, {instance_name}'].append(deepcopy(local_search_with_list))

            ##################################################################
            #LocalSearchCandidateMoves
            ls_candidates_moves = LocalSearchCandidateMoves(instance)
            ls_candidates_moves.neighborhood = 'edges' 

            #candidates moves, random
            ls_candidates_moves.first_solution = random_cycle.first_solution[:]
            ls_candidates_moves.second_solution = random_cycle.second_solution[:]
            time = ls_candidates_moves.solve(n_candidats = 8)
            times[f'CM, {instance_name}'].append(time)
            scores[f'CM, {instance_name}'].append(deepcopy(ls_candidates_moves))

    
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
    save_string_fn(save_string, 'local_search_and_candidates_moves_results', None)


if __name__ == "__main__":
    main()