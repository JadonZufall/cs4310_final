from typing import Optional
import random

import pygame


from src.res.graph_visual import GraphVisual
from src.res.event_system import EventHandler, EventListener
from src.obj.graph import Graph
from src.obj.node import Node
from src.tests.graph_generator import generate_complete_graph, generate_random_graph, generate_tree_graph

        



is_running: bool = True
visual = GraphVisual(win_size=(500, 500))
event_handler: EventHandler = EventHandler()
tgraph: Graph = Graph()

def exit_visual(dt: int, event: pygame.event.Event) -> None:
    global is_running
    is_running = False
event_handler.bind_to_event(pygame.QUIT, exit_visual)


for i in range(0, 10):
    tgraph.add_node(Node(random.randint(0, 10), random.randint(50, 450), random.randint(50, 450)))


for _ in range(0, random.randint(0, 25)):
    n1 = tgraph.get_random_node()
    n2 = tgraph.get_random_node()
    if n1 == n2:
        continue
    tgraph.add_edge(n1, n2, False, False)

tgraph = generate_random_graph()

while is_running:
    dt = visual.wait(fps=60)
    event_handler.update(dt=dt)
    visual.draw(graph=tgraph)