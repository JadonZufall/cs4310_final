from src.obj.node import Node

class Graph:
    def __init__(self, nodes: list[Node]=[]) -> None:
        self._nodes: list[Node] = nodes
