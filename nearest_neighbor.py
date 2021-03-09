import numpy as np
from utils.utils import read_instances, build_distance_matrix, get_name
from math import isnan, isinf

GLOBAL_PATH = 'Instances\\'

def get_matrix_without_indicies(distance_matrix, indicies):
    indicies = np.array(indicies)
    #distance_matrix[indicies, :] = np.float('inf')
    distance_matrix[:, indicies] = np.float('inf')
    return distance_matrix
     

def greedy_cycle(distance_matrix, num, start_node_idx):
    cycle = [start_node_idx]
    cycle.append(np.argmin(distance_matrix[start_node_idx]))
    while len(cycle) < num:
        candidates = list()
        for idx, check_node in enumerate(cycle):
            distance = float('inf')
            for best_node in range(len(distance_matrix[check_node])):
                if isinf(distance_matrix[check_node][best_node]) or best_node in cycle:
                    continue
                temp = distance_matrix[check_node, best_node] + distance_matrix[best_node, cycle[(idx+1) % len(cycle)]] - distance_matrix[check_node, cycle[(idx+1) % len(cycle)]]
                if not isnan(temp) and temp < distance:
                    distance = temp
                    best_node_final = best_node
            candidates.append((idx, best_node_final, distance))
        node = min(candidates, key = lambda el: el[2])
        cycle = cycle[:node[0]+1] + [node[1]] + cycle[node[0]+1:]
        
    return cycle

def main():
    ins_name = get_name(1)
    path = GLOBAL_PATH + ins_name
    point_dict = read_instances(path)
    num1 = len(point_dict) // 2
    num2 = len(point_dict) - num1
    
    distance_matrix = build_distance_matrix(point_dict)
    
    first_start_node_idx = np.random.choice(list(point_dict.keys()))
    second_start_node_idx = np.where(np.isinf(distance_matrix[first_start_node_idx, :]),-np.Inf, distance_matrix[first_start_node_idx, :]).argmax()

    first_start_node = (point_dict[first_start_node_idx].x, point_dict[first_start_node_idx].y)
    second_start_node = (point_dict[second_start_node_idx].x, point_dict[second_start_node_idx].y)

    cycle1 = greedy_cycle(distance_matrix, num1, first_start_node_idx)
    print(cycle1)
    distance_matrix = get_matrix_without_indicies(distance_matrix, cycle1)
    cycle2 = greedy_cycle(distance_matrix, num2, second_start_node_idx)
    print(cycle2)

    

if __name__ == "__main__":
    main()
