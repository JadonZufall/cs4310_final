from src.obj.graph import Graph, get_paths, get_path_length
from src.obj.node import Node, Edge

def bellman_ford(graph: Graph, start: Node, end: Node):
    nodes = graph.get_nodes()
    edges: list[Edge] = []
    for n in nodes:
        for e in n.get_edges():
            edges.append(e)
    
    distances = []
    predecessor = []
    for _ in range(0, len(nodes)):
        distances.append(-1)
        predecessor.append(None)

    distances[start._index] = 0
    
    # Relax edges
    for i in range(len(nodes)):
        for e in edges:
            w = e._weight
            src = e._src
            dst = e._dst
            if distances[src._index] + w < distances[dst._index]:
                distances[src._index] = distances[dst._index] + w
                predecessor[src._index] = dst
    
    

    # Check for negative weights
    for e in edges:
        w = e._weight
        src = e._src
        dst = e._dst
        if distances[dst._index] + w < distances[src._index]:
            predecessor[src._index] = src
            visited = [False for i in range(len(nodes))]
            visited[dst._index] = True
            while not visited[dst._index]:
                visited[dst._index] = True
                dst = predecessor[dst._index]
            ncycle = [dst]
            while src != dst:
                ncycle = ncycle + [src]
                src = predecessor[src._index]
    return distances, predecessor
    