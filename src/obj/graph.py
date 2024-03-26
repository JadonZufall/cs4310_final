from src.obj.node import Node
from typing import Optional
import random

XMIN = 0
XMAX = 100
YMIN = 0
YMAX = 100

class Graph:
    def __init__(self, nodes: list[Node]=[]) -> None:
        self._nodes: list[Node] = nodes

    def contains(self, instance: Node) -> bool:
        return instance in self._nodes
    
    def add_node(self, node: Optional[Node] = None):
        # Generate a random new node
        if node is None:
            self._nodes.append(Node(None, random.randrange(XMIN, XMAX), random.randrange(YMIN, YMAX)))
        else: 
            self._nodes.append(node)


    def add_edge(self, node1: Node, node2: Node, weighted: bool, directed: bool) -> None:
        if self.contains(node1) and self.contains(node2):
            node1.add_edge(node2, weighted)
            if not directed:
                node2.add_edge(node1, weighted)
    
    def get_nodes(self) -> list[Node]:
        return self._nodes
    
    def get_random_node(self) -> Node:
        return random.choice(self._nodes) if len(self._nodes) != 0 else None
    
    def print(self):
        for node in self._nodes:
            edges = node.get_edges()
            for edge in edges:
                print(f"{node.get_value()} {edge.get_destination().get_value()}")
    
    def merge(self, g2: 'Graph', n1: Node, n2: Node, weighted: bool, directed: bool):
        for node in g2.get_nodes():
            self.add_node(node)
        self.add_edge(n1, n2, weighted, directed)