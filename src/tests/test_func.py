import unittest
import random
from src.obj.graph import Graph
from src.obj.node import Node

class TestPathfindingFunctions(unittest.TestCase):
    def test_random_shortest_path(self) -> None:
        test_nodes: list[Node] = []
        for i in range(0, 100):
            rx: int = random.randint(0, 1_000)
            ry: int = random.randint(0, 1_000)
            test_nodes.append(Node(value=f"node #{i}", x=rx, y=ry))
        test_graph: Graph = Graph(nodes=test_nodes)
        for i in range(0, 100):
            num_edges = random.randint(0, 10)
            for j in range(0, num_edges):
                ji = random.randint(0, len(test_nodes))
                if ji == i:
                    continue
                test_nodes[i].add_edge(test_nodes[ji])
        start_node: Node = test_nodes[random.randint(0, len(test_nodes))]
        end_node: Node = test_nodes[random.randint(0, len(test_nodes))]
        while start_node is end_node:
            end_node = test_nodes[random.randint(0, len(test_nodes))]
        