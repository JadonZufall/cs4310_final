from src.obj.graph import Graph
import src.obj.graph as graph
from src.obj.node import Node
import random
import copy
from fibheap import Fheap

MAX_NODES = 31

def generate_tree_graph(num_nodes: int = random.randrange(0, MAX_NODES), weighted: bool = True, directed: bool = False) -> Graph:
    nodes = [Node(str(x), random.randrange(graph.XMIN, graph.XMAX), random.randrange(graph.YMIN, graph.YMAX)) for x in range(0, num_nodes)]
    graphs = [Graph([nodes[i]]) for i in range(0, num_nodes)]
    while len(graphs) != 1:
        g1 = random.choice(graphs)
        graphs.remove(g1)
        g2 = random.choice(graphs)
        g2.merge(g1, g2.get_random_node(), g1.get_random_node(), weighted, directed)
    return graphs[0]