import numpy as np
from utils.utils import read_instances, build_distance_matrix, get_name
from math import isnan, isinf

GLOBAL_PATH = 'Instances\\'

def get_matrix_without_indicies(distance_matrix, indicies):
    indicies = np.array(indicies)
    #distance_matrix[indicies, :] = np.float('inf')
    distance_matrix[:, indicies] = np.float('inf')
    return distance_matrix
     

def greedy_cycle_with_regret(distance_matrix, num, start_node_idx, k_regret = 2):
    cycle = [start_node_idx]
    cycle.append(np.argmin(distance_matrix[start_node_idx]))
    while len(cycle) < num:
        cost = list()
        idxs = list()
        for v in range(len(distance_matrix)):
            c = list()
            if v in cycle:
                continue
            for k in cycle:
                if isinf(distance_matrix[k, v]):
                    continue
                temp = distance_matrix[k, v] + distance_matrix[v, (k+1)%len(cycle)] - distance_matrix[k, (k+1)%len(cycle)]
                if not isinf(temp):
                    c.append((temp, v, k))
            if c:
                c = sorted(c, key = lambda el: el[0])
                cost.append(c)

        regret = list()
        for c in cost:
            suma = 0
            for i in range(min(k_regret, len(c))):
                suma += c[i][0]
            regret.append(suma - c[0][0])
        v_best = np.argmax(regret)
        i = cost[v_best][0][2]
        best = cost[v_best][0][1]
        cycle = cycle[:i+1] + [best] + cycle[i+1:]
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

    cycle1 = greedy_cycle_with_regret(get_matrix_without_indicies(distance_matrix, [second_start_node_idx]), num1, first_start_node_idx)
    print(cycle1)
    distance_matrix = get_matrix_without_indicies(distance_matrix, cycle1)
    cycle2 = greedy_cycle_with_regret(distance_matrix, num2, second_start_node_idx)
    print(cycle2)
    

if __name__ == "__main__":
    main()
