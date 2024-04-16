from src.obj.graph import Graph
from src.obj.node import Node, Edge
from fibheap import Fheap
import heapq

def dijkstra(graph: Graph, start: Node):
    # Create a priority queue of edges to consider
    pq = []
    heapq.heappush(pq, (0,Edge(src=None, dst=start, weighted=False)))

    # Keep track of each node's previous node
    prev = [None] * graph.get_num_nodes()
    distances = [float('inf')] * graph.get_num_nodes()
    distances[start._index] = 0

    # Repeatedly pop from priority queue
    while pq:
        current_distance, current_edge = heapq.heappop(pq)

        previous = current_edge._src
        current = current_edge._dst

        if (prev[current._index] == None):
            if previous != None:
                prev[current._index] = previous._index

            adjacent_edges = current.get_edges()

            for adjacent_edge in adjacent_edges:
                weight = adjacent_edge._weight
                prospect = adjacent_edge._dst

                if distances[prospect._index] > current_distance + weight:
                    distances[prospect._index] = current_distance + weight
                    heapq.heappush(pq, (distances[prospect._index], adjacent_edge))

    return distances, prev