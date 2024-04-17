import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from src.tests.graph_generator import generate_random_graph


def start():
    graph = generate_random_graph(num_nodes=10)
    nodes = graph.get_nodes()
    g = nx.DiGraph()
    fedges = []
    for src_idx, n in enumerate(nodes):
        edges = n.get_edges()
        for e in edges:
            dst_idx: int = nodes.index(e._dst)
            fedges.append((str(src_idx), str(dst_idx)))
    g.add_edges_from(fedges)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap("jet"))
    nx.draw_networkx_edges(g, pos, arrows=False)
    plt.show()
    