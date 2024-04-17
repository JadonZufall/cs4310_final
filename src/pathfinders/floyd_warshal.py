import math
from src.obj.graph import Graph
from src.obj.graph import Node



def floyd_warshal(graph: Graph, start: Node, end: Node) -> None:
    nodes: list[Node] = graph.get_nodes()
    N: int = graph.get_num_nodes()
    V: int = sum([m.get_number_edges() for m in nodes])
    
    cost_matrix: list[list[float]] = [[math.inf] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if nodes[j] not in nodes[i].get_neighbors():
                cost_matrix[i][j] = math.inf
            else:
                p0 = nodes[i].get_coordinates()
                p1 = nodes[i].get_coordinates()
                cost_matrix[i][j] = math.dist(p0, p1)
    
    