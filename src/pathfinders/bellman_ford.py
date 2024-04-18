from src.obj.graph import Graph, get_paths, get_path_length
from src.obj.node import Node, Edge

def bellman_ford(graph: Graph, start: Node, end: Node):
    nodes = graph.get_nodes()
    edges: list[Edge] = []
    for n in nodes:
        for e in n.get_edges():
            edges.append(e)
    edges = list(set(edges))
    
    distances = []
    predecessor = []
    for _ in range(0, len(nodes)):
        distances.append(-1)
        predecessor.append(None)

    distances[nodes.index(start)] = 0
    
    # Relax edges
    for i in range(len(edges) - 1):
        for e in edges:
            w = e._weight
            src = e._src
            dst = e._dst
            if distances[nodes.index(src)] + w < distances[nodes.index(dst)]:
                distances[nodes.index(src)] = distances[nodes.index(dst)] + w
                predecessor[nodes.index(src)] = dst
    
    

    # Check for negative weights
    for e in edges:
        w = e._weight
        src = e._src
        dst = e._dst
        if distances[nodes.index(dst)] + w < distances[nodes.index(src)]:
            predecessor[nodes.index(src)] = src
            visted = [False for i in range(len(nodes))]
            visited[nodes.index(dst)] = True
            while not visted[nodes.index(dst)]:
                visted[nodes.index(dst)] = True
                dst = predecessor[nodes.index(dst)]
            ncycle = [dst]
            while src != dst:
                ncycle = ncycle + [src]
                src = predecessor[nodes.index(src)]
    return distances, predecessor
    