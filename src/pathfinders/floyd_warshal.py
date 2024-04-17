import math
from src.obj.graph import Graph
from src.obj.graph import Node


def floyd_warshall(graph: Graph):
    nodes = graph._nodes
    num_nodes = len(nodes)

    # Initialize adjacency matrix
    dist = [[float('inf') for j in range(num_nodes)] for i in range(num_nodes)] 
    dist[0][0] = 0


    for i in range(num_nodes):
        dist[i][i] = 0.0

    for node in nodes:
        edges = node._edges
        for edge in edges:
            dist[edge._src._index][edge._dst._index] = edge._weight

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                dist[i][j] = min((dist[i][j], dist[i][k] + dist[k][j]))

    return dist

    
    