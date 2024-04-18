from src.obj.graph import Graph, get_paths, get_path_length
from src.obj.node import Node, Edge
from src.pathfinders.dijkstra import dijkstra
from src.tests.graph_generator import generate_random_graph
from itertools import count

import heapq

def yen(graph: Graph, start: Node, end: Node, K: int):

    # Calculate the initial shortest path
    dist, prev, added_edges, considered = dijkstra(graph, start=start, end=end)
    initial_paths = get_paths(prev)

    # Initialize our paths and their lengths
    paths = [initial_paths[end._index]]
    lengths = [dist[end._index]] 

    c = count()
    B = []

    # Calculate for every K remaining
    for i in range(1, K):
        # Consider every spur node
        for j in range(0, len(paths[-1]) - 1):
            # Get the spur node and the root path
            spurNode = paths[-1][j]
            root_path = paths[-1][:j + 1]

            # Remove the links that are part of the previous shortest paths which share the same root path.
            edges_removed = []
            for path in paths:
                if len(path) > j and root_path == path[:j + 1]:
                    edge1 = graph.disable_edge(path[j], path[j+1])
                    edge2 = graph.disable_edge(path[j+1], path[j])
                    if edge1 is not None:
                        edges_removed.append(edge1)
                    if edge2 is not None:
                        edges_removed.append(edge2)


            # Remove all root path nodes except spur node
            nodes_removed = []
            for n in range(len(root_path) - 1):
                # Get the node to remove
                node_index = root_path[n]
                node = graph.disable_node(node_index)
                if node is not None:
                    nodes_removed.append(node)

            distance, previous, junk, junky = dijkstra(graph, graph._nodes[spurNode], end)
            # Only consider the spur path if it reached the target
            if distance[end._index] != float('inf'):
                target_path = root_path[:-1] + get_paths(previous)[end._index]
                target_length = get_path_length(graph, target_path)
                if (target_length, target_path) not in B:
                    heapq.heappush(B, (target_length, target_path))
            
            for edge in edges_removed:
                edge.enable = True
            for node in nodes_removed:
                node.enabled = True
            
        if len(B) != 0:
            stuff = heapq.heappop(B)
            lengths.append(stuff[0])
            paths.append(stuff[1])
        else:
            break
    return lengths, paths