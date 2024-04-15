import pygame
from src.res.graph_visual import GraphVisual
from src.obj.graph import Graph
from src.obj.node import Node

if __name__ == "__main__":
    import random
    is_running: bool = True
    visual = GraphVisual(win_size=(500, 500))
    tgraph: Graph = Graph()
    for i in range(0, 10):
        tgraph.add_node(Node(random.randint(0, 10), random.randint(50, 450), random.randint(50, 450)))
    for _ in range(0, random.randint(0, 25)):
        n1 = tgraph.get_random_node()
        n2 = tgraph.get_random_node()
        if n1 == n2:
            continue
        tgraph.add_edge(n1, n2, False, False)
    while is_running:
        visual.wait(fps=60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            else:
                visual.event(event)
        visual.draw(graph=tgraph)