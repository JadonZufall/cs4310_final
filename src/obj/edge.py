from typing import Optional
from src.obj.node import Node

class Edge:
    """ Represents a connection between two nodes. """
    def __init__(self, src: Optional["Node"], dst: Optional["Node"], weight: float=1.0) -> None:
        """ Construct a new Edge instance. """
        self._src: "Node" = src
        self._dst: "Node" = dst
        self._weight: float = weight
    
    def reverse(self) -> "Edge":
        """ Make the edge go in the reverse direction. """
        return Edge(src=self._dst, dst=self._src, weight=self._weight)
