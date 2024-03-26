from src.obj.node import Node

class Graph:
    def __init__(self, nodes: list[Node]=[]) -> None:
        self._nodes: list[Node] = nodes

    def contains(self, instance: Node) -> bool:
        return instance in self._nodes
    
    def create_edge(self, node1: Node, node2: Node, weighted: bool, directed: bool) -> None:
        if self.contains(node1) and self.contains(node2):
            node1.add_edge(node2, weighted)
            if not directed:
                node2.add_edge(node1, weighted)