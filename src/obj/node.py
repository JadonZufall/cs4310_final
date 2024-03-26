from typing import Optional
from edge import Edge
from node import Node



class Node:
    def __init__(self, value: Optional[str]=None, x: int = 0, y: int = 0) -> None:
        self._value: Optional[str] = value
        self._edges: list[Edge] = None
        self._x: int = x
        self._y: int = y

    def get_coordinates(self) -> list[int]:
        return self._x, self._y

    def add_edge(self, dst: Node, weighted: bool) -> None:
        self._edges.append(Edge(self, dst, weighted))

