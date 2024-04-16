from typing import Optional
from math import sqrt as SQRT
from math import pow as POW

class Edge:
    """ Represents a connection between two nodes. """
    def __init__(self, src: 'Node', dst: 'Node', weighted: bool) -> None:
        """ Construct a new Edge instance. """
        self._src: Node = src
        self._dst: Node = dst


        if not weighted:
            self._weight: float = 1.0
        else:
            self._weight: float = SQRT(POW(src._x - dst._x, 2) + POW(src._y - dst._y, 2))
    
    def __repr__(self):
        return repr((self._src, self._dst, self._weight))

    def __lt__(self, other):
        return self._weight < other._weight

    def contains(self, instance: 'Node') -> bool:
        return instance is self._src or instance is self._dst
    
    def reverse(self) -> "Edge":
        """ Make the edge go in the reverse direction. """
        return Edge(src=self._dst, dst=self._src, weight=self._weight)
    
    def get_source(self) -> 'Node':
        return self._src
    
    def get_destination(self) -> 'Node':
        return self._dst
    
    def get_weight(self) -> float:
        return self._weight

class Node:
    def __init__(self, value: Optional[str]=None, x: int = 0, y: int = 0, index: int = 0) -> None:
        self._value: Optional[str] = value
        self._edges: list[Edge] = []
        self._x: int = x
        self._y: int = y
        self._index = index
    
    def __repr__(self):
        return repr((self._value, self._x, self._y))

    def get_coordinates(self) -> list[int]:
        return self._x, self._y

    def get_value(self) -> str:
        return self._value

    def add_edge(self, dst: 'Node', weighted: bool) -> None:
        self._edges.append(Edge(self, dst, weighted))

    
    def get_edges(self) -> list[Edge]:
        return self._edges
    
    def get_neighbors(self) -> list['Node']:
        return [edge.get_destination() for edge in self._edges]
    
    def set_index(self, index: int) -> None:
        self._index = index

    def get_index(self) -> int:
        return self._index
    
    def reorder_adjacents(self):
        self._edges.sort(key = lambda edge: edge._dst._value)
