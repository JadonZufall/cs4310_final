from typing import Optional
from src.obj.node import Node
from math import sqrt as SQRT
from math import pow as POW

class Edge:
    """ Represents a connection between two nodes. """
    def __init__(self, src: Node, dst: Node, weighted: bool) -> None:
        """ Construct a new Edge instance. """
        self._src: Node = src
        self._dst: Node = dst

        """ Calculate weight (1 for unweighted graphs)"""
        src_x, src_y = src.get_coordinates()
        dst_x, dst_y = src.get_coordinates()
        self._weight: float = 1.0 if not weighted else SQRT(POW(src_x - dst_x, 2) + POW(src_y - dst_y, 2))
    
    def contains(self, instance: Node) -> bool:
        return instance is self._src or instance is self._dst
    
    def reverse(self) -> "Edge":
        """ Make the edge go in the reverse direction. """
        return Edge(src=self._dst, dst=self._src, weight=self._weight)
    
    def get_source(self) -> Node:
        return self._src
    
    def get_destination(self) -> Node:
        return self._dst
    
    def get_weight(self) -> float:
        return self._weight

