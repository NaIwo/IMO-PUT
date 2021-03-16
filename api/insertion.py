

class Insertion():

    def __init__(self, node_to_insert, insertion_cost, place_in_cyce):
        self._node_to_insert = node_to_insert
        self._insertion_cost = insertion_cost
        self._place_in_cyce = place_in_cyce

    @property
    def node_to_insert(self):
        return self._node_to_insert

    @property
    def insertion_cost(self):
        return self._insertion_cost
    
    @property
    def place_in_cyce(self):
        return self._place_in_cyce

    def __str__(self):
        return f'Insertion(node_to_insert={self._node_to_insert}, insertion_cost={self._insertion_cost}, place_in_cyce={self._place_in_cyce})'

    def __repr__(self):
        return self.__str__()
