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
from approaches.local_search_cycle.local_search_iterated import LocalSearchIterated
from approaches.local_search_cycle.local_search_with_list_heuristic import LocalSearchWithList

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

def get_ls(times, scores, instance):
    unavailable_points = list()
    for local_number in range(read_input(2)):
        print(f'\t->  Local iteration number: {local_number+1}')
        first_start_node = random.choice( list( set(list(instance.point_dict.keys())) - set(unavailable_points) ) )
        unavailable_points.append(first_start_node)
        second_start_node = np.argmax(instance.matrix[first_start_node])
        unavailable_points.append(second_start_node)

        #Get random solution
        random_cycle = Random(instance, seed = None)
        random_cycle.solve(first_start_node, second_start_node)

        ##################################################################
        #Local Search
        local_search = LocalSearch(instance)
        local_search.neighborhood = 'edges' 

        #steepest, edges, random
        local_search.first_solution = random_cycle.first_solution[:]
        local_search.second_solution = random_cycle.second_solution[:]
        time = local_search.solve(method = 'steepest')
        times[f'MSLS, {instance.instance_name}'].append(time)
        scores[f'MSLS, {instance.instance_name}'].append(deepcopy(local_search))

def main():
    times_number = get_value()

    times = defaultdict(list)
    scores = defaultdict(list)
    
    for instance_name in ['kroA200', 'kroB200']:
        instance = Instance(name = instance_name)
        instance.compute_matrix()

        ####################################
        get_ls(times, scores, instance)
        #####################################
        max_time = np.mean(times[f'MSLS, {instance_name}'])
        unavailable_points = list()
        for number in range(times_number):

            first_start_node = random.choice( list( set(list(instance.point_dict.keys())) - set(unavailable_points) ) )
            second_start_node = np.argmax(instance.matrix[first_start_node])
            unavailable_points.append(first_start_node)
            unavailable_points.append(second_start_node)
            #Get random solution
            random_cycle = Random(instance, seed = None)
            random_cycle.solve(first_start_node, second_start_node)

            print(f'Global iteration number: {number+1}')

            ##################################################################
            #ILS1
            local_search = LocalSearchIterated(instance)
            local_search.neighborhood = 'edges' 
            #for num in range(3,25):
            local_search.first_solution = random_cycle.first_solution[:]
            local_search.second_solution = random_cycle.second_solution[:]
            time = local_search.solve_ils1(num_moves = 20, max_time = max_time)
            times[f'ILS1, {instance_name}'].append(time)
            scores[f'ILS1, {instance_name}'].append(deepcopy(local_search))

            ##################################################################
             #ILS2
            local_search = LocalSearchIterated(instance)
            local_search.neighborhood = 'edges' 
            #for num in range(3,25):
            local_search.first_solution = random_cycle.first_solution[:]
            local_search.second_solution = random_cycle.second_solution[:]
            time = local_search.solve_ils2(num_nodes = 40, max_time = max_time)
            times[f'ILS2, {instance_name}'].append(time)
            scores[f'ILS2, {instance_name}'].append(deepcopy(local_search))


        
        
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
    save_string_fn(save_string, 'ILSX_results', None)





if __name__ == "__main__":
    main()