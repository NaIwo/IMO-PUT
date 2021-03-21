

class Replacement():

    def __init__(self, first_cycle, second_cycle, score):
        self._first_cycle = first_cycle
        self._second_cycle = second_cycle
        self._score = score

    @property
    def first_cycle(self):
        return self._first_cycle

    @property
    def second_cycle(self):
        return self._second_cycle
    
    @property
    def score(self):
        return self._score


    def __str__(self):
        return f'Replacement(first_cycle={self._first_cycle}, second_cycle={self._second_cycle}, score={self._score})'

    def __repr__(self):
        return self.__str__()
