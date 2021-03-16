import numpy as np
from collections import namedtuple

class Instance():

    PATH = 'Instances\\{}.tsp'

    def __init__(self, name):
        self.instance_name = name
        self.instance_path = Instance.PATH.format(name)
        self._point_dict = dict()
        self._matrix: np.ndarray = None
    
    def _read_instance_file(self):
        point = namedtuple('Point', ['x', 'y'])
        start_reading = False
        with open(self.instance_path, 'r') as f:
            for line in f.readlines():
                if line == 'EOF':
                    start_reading = False
                if start_reading:
                    temp = list(map(int, line.split()))
                    self._point_dict[int(temp[0]) - 1] = point(temp[1], temp[2])
                if line.strip() == 'NODE_COORD_SECTION':
                    start_reading = True

    def compute_matrix(self):
        self._read_instance_file()
        self._matrix = np.zeros((len(self._point_dict), len(self._point_dict)))
        for row_idx, _ in enumerate(self._point_dict):
            for col_idx, _ in enumerate(self._point_dict):
                distance = np.sqrt((self._point_dict[row_idx].x - self._point_dict[col_idx].x)**2 + (self._point_dict[row_idx].y - self._point_dict[col_idx].y)**2)
                self._matrix[row_idx, col_idx] = round(distance)
    
    @property
    def matrix(self):
        return self._matrix
    
    @property
    def point_dict(self):
        return self._point_dict

    @matrix.setter
    def matrix(self, new_matrix):
        self._matrix = new_matrix