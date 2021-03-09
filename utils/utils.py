from collections import namedtuple
import sys
import numpy as np

def get_name(num):
    try:
        name = sys.argv[num]
    except IndexError:
        raise IndexError
    return name

def read_instances(path):
    point = namedtuple('Point', ['x', 'y'])
    points = dict()
    start_reading = False
    with open(path, 'r') as f:
        for line in f.readlines():
            if line == 'EOF':
                start_reading = False
            if start_reading:
                temp = list(map(int, line.split()))
                points[temp[0]] = point(temp[1], temp[2])
            if line.strip() == 'NODE_COORD_SECTION':
                start_reading = True
    return points

def build_distance_matrix(point_dict):
    distance_matrix = list()
    for idx1 in range(1, len(point_dict) + 1):
        temp = list()
        for idx2 in range(1, len(point_dict) + 1):
            distance = np.sqrt((point_dict[idx1].x - point_dict[idx2].x)**2 + (point_dict[idx1].y - point_dict[idx2].y)**2)
            if idx1 != idx2:
                temp.append(round(distance))
            else:
                temp.append(np.float('inf'))
        distance_matrix.append(temp)
    return np.array(distance_matrix)