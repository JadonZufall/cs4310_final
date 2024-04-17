import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
from IPython import display


from src.tests.graph_generator import generate_random_graph


def generate_gif(fr, graph, red_edges):
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
    nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap("jet"))
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

def animate():
    graph = generate_random_graph(num_nodes=10)
    fdat = [(str(random.randint(0, 10-1)), str(random.randint(0, 10-1))) for i in range(0, 100)]
    funcs = []
    for i, f in enumerate(fdat):
        funcs.append(PFunc(generate_gif, graph, red_edges=fdat[0:i]))
    
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
    video.save("out.mp4", fps=1)
    html = display.HTML(video.to_html5_video())
    with open("out.html", "w") as file:
        file.write(html.data)
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
    