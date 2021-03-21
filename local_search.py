import numpy as np
import random
import sys
from collections import defaultdict
from copy import deepcopy

from helpers.helpers import plot_result, save_string_fn
from api.instance import Instance
from approaches.local_search_cycle.local_search_heuristic import LocalSearch
from approaches.local_search_cycle.random_local_search import RandomLocalSearch
from approaches.greedy_cycle.greedy_heuristic import Greedy
from approaches.random_cycle.random_heuristic import Random

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

def plot_random(random_cycle):
    plot_title = f'{random_cycle.algorithm}, {random_cycle.instance.instance_name}, Distance: {random_cycle.compute_total_cost()}'
    save_name = '{}'.format(random_cycle.instance.instance_name)
    plot_result(random_cycle, plot_title, save_name)

def plot_best(instance, key):
    plot_title = f'{instance.algorithm}, {key}, Distance: {instance.compute_total_cost()}'
    save_name = '{}'.format(key)
    plot_result(instance, plot_title, save_name)

def main():
    times_number = get_value()

    times = defaultdict(list)
    scores = defaultdict(list)
    
    for instance_name in ['kroA100', 'kroB100']:
        instance = Instance(name = instance_name)
        instance.compute_matrix()
        
        ##Get greedy solution
        first_start_node = 92 if instance_name == 'kroA100' else 72 #Najlepsze startowe wierzchołki dla intsancji Greedy (poprzednie zadanie)
        second_start_node = np.argmax(instance.matrix[first_start_node])
        greedy_cycle = Greedy(instance, regret = 2)
        greedy_cycle.solve(first_start_node, second_start_node)

        for _ in range(times_number):
            #Get random solution
            first_start_node = random.choice(list(instance.point_dict.keys()))
            second_start_node = np.argmax(instance.matrix[first_start_node])
            random_cycle = Random(instance, seed = None)
            random_cycle.solve(first_start_node, second_start_node)
            #plot_random(random_cycle)

            #Local Search
            local_search = LocalSearch(instance)

            #streepest, nodes, greedy_cycle
            local_search.first_solution = greedy_cycle.first_solution
            local_search.second_solution = greedy_cycle.second_solution
            time = local_search.solve(method = 'steepest')
            times[f'streepest, nodes, greedy_cycle, {instance_name}'].append(time)
            scores[f'streepest, nodes, greedy_cycle, {instance_name}'].append(deepcopy(local_search))

            #greedy, nodes, greedy_cycle
            local_search.first_solution = greedy_cycle.first_solution
            local_search.second_solution = greedy_cycle.second_solution
            time = local_search.solve(method = 'greedy')
            times[f'greedy, nodes, greedy_cycle, {instance_name}'].append(time)
            scores[f'greedy, nodes, greedy_cycle, {instance_name}'].append(deepcopy(local_search))

            #streepest, nodes, random
            local_search.first_solution = random_cycle.first_solution
            local_search.second_solution = random_cycle.second_solution
            time = local_search.solve(method = 'steepest')
            times[f'streepest, nodes, random, {instance_name}'].append(time)
            scores[f'streepest, nodes, random, {instance_name}'].append(deepcopy(local_search))

            #greedy, nodes, random
            local_search.first_solution = random_cycle.first_solution
            local_search.second_solution = random_cycle.second_solution
            time = local_search.solve(method = 'greedy')
            times[f'greedy, nodes, random, {instance_name}'].append(time)
            scores[f'greedy, nodes, random, {instance_name}'].append(deepcopy(local_search))

            local_search.neighborhood = 'edges' 

            #streepest, edges, greedy_cycle
            local_search.first_solution = greedy_cycle.first_solution
            local_search.second_solution = greedy_cycle.second_solution
            time = local_search.solve(method = 'steepest')
            times[f'streepest, edges, greedy_cycle, {instance_name}'].append(time)
            scores[f'streepest, edges, greedy_cycle, {instance_name}'].append(deepcopy(local_search))

            #greedy, edges, greedy_cycle
            local_search.first_solution = greedy_cycle.first_solution
            local_search.second_solution = greedy_cycle.second_solution
            time = local_search.solve(method = 'greedy')
            times[f'greedy, edges, greedy_cycle, {instance_name}'].append(time)
            scores[f'greedy, edges, greedy_cycle, {instance_name}'].append(deepcopy(local_search))

            #streepest, edges, random
            local_search.first_solution = random_cycle.first_solution
            local_search.second_solution = random_cycle.second_solution
            time = local_search.solve(method = 'steepest')
            times[f'streepest, edges, random, {instance_name}'].append(time)
            scores[f'streepest, edges, random, {instance_name}'].append(deepcopy(local_search))

            #greedy, edges, random
            local_search.first_solution = random_cycle.first_solution
            local_search.second_solution = random_cycle.second_solution
            time = local_search.solve(method = 'greedy')
            times[f'greedy, edges, random, {instance_name}'].append(time)
            scores[f'greedy, edges, random, {instance_name}'].append(deepcopy(local_search))
    
    save_string = '\n'
    worst_time = float('inf')
    for key in scores.keys():
        best = min(scores[key], key=lambda el: el.compute_total_cost())
        costs = list( map(lambda el: el.compute_total_cost(), scores[key]) )
        save_string += f'Version: {key}\nMean: {np.mean(costs)}\nMin: {min(costs)}\nMax: {max(costs)}\n\n|TIMES|\n'
        save_string += f'\nMean: {np.mean(times[key])}\nMin: {min(times[key])}\nMax: {max(times[key])}\n\n==========\n\n'
        if np.mean(times[key]) < worst_time:
            worst_time = np.mean(times[key])
        plot_best(best, key)
    
    print(save_string)
    save_string_fn(save_string, 'computation_results', best)

    for instance_name in ['kroA100', 'kroB100']:
        instance = Instance(name = instance_name)
        instance.compute_matrix()
        random_local_search = RandomLocalSearch(instance)
        random_local_search.first_solution = greedy_cycle.first_solution
        random_local_search.second_solution = greedy_cycle.second_solution
        random_local_search.solve(worst_time)
        plot_best(random_local_search, instance_name)


if __name__ == "__main__":
    main()