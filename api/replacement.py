import functools

@functools.total_ordering
class Replacement():

    def __init__(self, first_cycle, second_cycle, score, node1 = None, node2 = None, operation_type = None, main_cycle = 'Both'):
        self._first_cycle = first_cycle
        self._second_cycle = second_cycle
        self._score = score
        self._node1 = node1
        self._node2 = node2
        self._operation_type = operation_type
        self._main_cycle = main_cycle

    @property
    def first_cycle(self):
        return self._first_cycle

    @first_cycle.setter
    def first_cycle(self, first_cycle):
        self._first_cycle = first_cycle

    @property
    def second_cycle(self):
        return self._second_cycle

    @second_cycle.setter
    def second_cycle(self, second_cycle):
        self._second_cycle = second_cycle
    
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score
    
    @property
    def node1(self):
        return self._node1
    @property
    def node2(self):
        return self._node2
    @property
    def operation_type(self):
        return self._operation_type
    @property
    def main_cycle(self):
        return self._main_cycle

    def __str__(self):
        if self._operation_type is None:
            return f'Replacement(first_cycle={self._first_cycle}, second_cycle={self._second_cycle}, score={self._score})'
        else:
            return f'Replacement(first_cycle={self._first_cycle}, second_cycle={self._second_cycle}, score={self._score}, node1={self._node1}, node2={self._node2}, operation_type={self._operation_type}, main_cycle={self._main_cycle})'

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self._score < other.score

    def __eq__(self, other):
        if isinstance(other, Replacement):
            return set(self._first_cycle) == set(other._first_cycle) and set(self._second_cycle) == set(other._second_cycle) and self._score == other.score
        else:
            return self._score == other.score