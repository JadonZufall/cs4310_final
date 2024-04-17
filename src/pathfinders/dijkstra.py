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

    # Keep track of the order in which edges are added and considered
    added_edges = []
    considered_edges = []

    # Repeatedly pop from priority queue
    while pq:
        # Get the next edge in the pqueue
        current_distance, current_edge = heapq.heappop(pq)

        # Get the 2 nodes of the edge
        previous = current_edge._src
        current = current_edge._dst

        # Only consider nodes which have not previously been reached
        if (prev[current._index] == None):
            # New edge has been added
            added_edges.append(current_edge)

            # Cannot set the start of the parent
            if current is not start:
                prev[current._index] = previous._index

            # Get all of the adjacent edges
            adjacent_edges = current.get_edges()

            # Keep track of which edges were considered
            considered = []

            # Check every adjacent edge
            for adjacent_edge in adjacent_edges:
                # Get the weight and the node
                weight = adjacent_edge._weight
                prospect = adjacent_edge._dst

                # If the distance is less than the current distance for that node, keep track of it
                if distances[prospect._index] > current_distance + weight:
                    considered.append(adjacent_edge)
                    distances[prospect._index] = current_distance + weight
                    heapq.heappush(pq, (distances[prospect._index], adjacent_edge))

            considered_edges.append(considered)

    return distances, prev, added_edges, considered_edges