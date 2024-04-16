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
            self._nodes.append(Node(None, random.randrange(XMIN, XMAX), random.randrange(YMIN, YMAX), len(self._nodes)))
        else: 
            node.set_index(len(self._nodes))
            self._nodes.append(node)


    def add_edge(self, node1: Node, node2: Node, weighted: bool, directed: bool) -> None:
        if self.contains(node1) and self.contains(node2):
            node1.add_edge(node2, weighted)
            if not directed:
                node2.add_edge(node1, weighted)
    
    def get_num_nodes(self) -> int:
        return len(self._nodes)

    def get_nodes(self) -> list[Node]:
        return self._nodes
    
    def get_random_node(self) -> Node:
        return random.choice(self._nodes) if len(self._nodes) != 0 else None
    
    def __str__(self):
        string = ""
        for node in self._nodes:
            edges = node.get_edges()
            for edge in edges:
                string += f"{node.get_value()} {edge.get_destination().get_value()}: {edge._weight}\n"
        return string
    
    def merge(self, g2: 'Graph', n1: Optional[Node] = None, n2: Optional[Node] = None, weighted: bool = True, directed: bool = False):
        for node in g2.get_nodes():
            self.add_node(node)
        if n1 is not None and n2 is not None:
            self.add_edge(n1, n2, weighted, directed)
    
    def reorder_nodes(self):
        self._nodes.sort(key=lambda node: node._value)
        for i in range(len(self._nodes)):
            self._nodes[i].reorder_adjacents()
            self._nodes[i]._index = i

def get_paths(previous_list):
    all_paths = []

    for i in range(len(previous_list)):
        current = i
        current_path = [i]
        while previous_list[current] != None:
            current = previous_list[current]
            current_path.append(current)
        current_path.reverse()
        all_paths.append(current_path)
    return all_paths