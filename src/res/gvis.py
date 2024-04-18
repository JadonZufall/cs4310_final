import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
from IPython import display


from src.tests.graph_generator import generate_random_graph


def generate_gif(fr, graph, red_edges, start_node, end_node):
    g = nx.DiGraph()
    nodes = graph.get_nodes()
    fedges = []
    for src_idx, n in enumerate(nodes):
        edges = n.get_edges()
        for e in edges:
            dst_idx: int = nodes.index(e._dst)
            fedges.append((str(src_idx), str(dst_idx)))
    
    red_edges = [i for i in red_edges]
    black_edges = [i for i in fedges]
    g.add_edges_from(fedges)
    pos = nx.spring_layout(g)
    g.add_node(nodes.index(start_node), node_color="green")
    g.add_node(nodes.index(end_node), node_color="red")
    
    nlist = list(map(lambda y: str(nodes.index(y)), list(filter(lambda x: x != start_node and x != end_node, nodes))))
    nx.draw_networkx_edge_labels(g, pos)
    nx.draw_networkx_nodes(g, pos, node_color="blue", nodelist=nlist)
    nx.draw_networkx_nodes(g, pos, node_color="green", nodelist=[str(nodes.index(start_node))], label="START")
    nx.draw_networkx_nodes(g, pos, node_color="red", nodelist=[str(nodes.index(end_node))], label="END")
    
    nx.draw_networkx_edges(g, pos, edgelist=black_edges, edge_color="black", arrows=False)
    nx.draw_networkx_edges(g, pos, edgelist=red_edges, edge_color="red", arrows=False)
    return g


class PGen:
    def __init__(self, gens: list) -> None:
        self.gens = gens
        self.i = -1
        
    def __call__(self, fr) -> None:
        self.i += 1
        if self.i >= len(self.gens):
            self.i = 0
        return self.gens[self.i](fr)


class PFunc:
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, fr) -> None:
        return self.f(fr, *self.args, **self.kwargs)

def animate(graph, fdat, out_path, start_node, end_node):
    funcs = []
    for i, f in enumerate(fdat):
        funcs.append(PFunc(generate_gif, graph, red_edges=fdat[0:i], start_node=start_node, end_node=end_node))
    
    g = nx.DiGraph()
    nodes = graph.get_nodes()
    fedges = []
    for src_idx, n in enumerate(nodes):
        edges = n.get_edges()
        for e in edges:
            dst_idx: int = nodes.index(e._dst)
            fedges.append((str(src_idx), str(dst_idx)))
    
    black_edges = [i for i in fedges]
    g.add_edges_from(fedges)
    pos = nx.spring_layout(g)
    
    
    def frame_animate(frame):
        nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap("jet"))
        nx.draw_networkx_edges(g, pos, edgelist=black_edges, edge_color="black", arrows=False)
        nx.draw_networkx_edges(g, pos, edgelist=fdat[0:min(frame, len(fdat)-1)], edge_color="red", arrows=False)
        print(frame)
    
    video = FuncAnimation(fig=plt.figure(), func=frame_animate, frames=30, interval=25)
    video.save(out_path, fps=1)
    plt.close()
    

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
    