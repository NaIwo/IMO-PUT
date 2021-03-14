import numpy as np
from utils.utils import read_instances, build_distance_matrix, get_name
from math import isnan, isinf
from copy import deepcopy

GLOBAL_PATH = 'Instances\\'

def get_matrix_without_indicies(distance_matrix, indicies, replace_number = np.float('inf')):
    indicies = np.array(indicies)
    #distance_matrix[indicies, :] = np.float('inf')
    distance_matrix[:, indicies] = replace_number
    return distance_matrix
     

def greedy_cycle_with_regret(distance_matrix, num, start_node_idx, k_regret = 2):
    cycle = [start_node_idx]
    cycle.append(np.argmin(distance_matrix[start_node_idx]))
    while len(cycle) < num:
        cost = list()
        cost_sorted = list()
        for k_i in range(distance_matrix.shape[0]):
            local_cost = list()
            for v_i, v in enumerate(cycle):
                if k_i in cycle:
                    continue
                if isinf(distance_matrix[v, k_i]):
                    continue
                v_2 = (v_i + 1) % len(cycle)
                if isinf(distance_matrix[k_i, cycle[v_2]]):
                    continue
                temp = distance_matrix[v, k_i] + distance_matrix[k_i, cycle[v_2]] - distance_matrix[v, cycle[v_2]]
                local_cost.append(temp)
            cost.append(local_cost)
            cost_sorted.append(sorted(local_cost))
        regret = [sum(v_cost[:k_regret]) - v_cost[0] if v_cost else 0 for v_cost in cost_sorted]
        v_best = np.argmax(regret)
        e = np.argwhere(cost[v_best] == cost_sorted[v_best][0])[0][0] + 1
        cycle = cycle[:e] + [v_best] + cycle[e:]

    return cycle
        
            
def main():
    ins_name = get_name(1)
    path = GLOBAL_PATH + ins_name
    point_dict = read_instances(path)
    num1 = len(point_dict) // 2
    num2 = len(point_dict) - num1
    
    distance_matrix = build_distance_matrix(point_dict)
    
    first_start_node_idx = np.random.choice(list(point_dict.keys())) - 1
    second_start_node_idx = np.where(np.isinf(distance_matrix[first_start_node_idx, :]),-np.Inf, distance_matrix[first_start_node_idx, :]).argmax()

    first_start_node = (point_dict[first_start_node_idx].x, point_dict[first_start_node_idx].y)
    second_start_node = (point_dict[second_start_node_idx].x, point_dict[second_start_node_idx].y)

    cycle1 = greedy_cycle_with_regret(get_matrix_without_indicies(deepcopy(distance_matrix), [second_start_node_idx]), num1, first_start_node_idx)
    print(cycle1)
    distance_matrix = get_matrix_without_indicies(distance_matrix, cycle1)
    cycle2 = greedy_cycle_with_regret(distance_matrix, num2, second_start_node_idx)
    print(cycle2)
    

if __name__ == "__main__":
    main()
