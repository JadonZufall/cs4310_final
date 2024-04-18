from src.obj.graph import Graph
from src.obj.node import Node, Edge
from src.tests.graph_generator import generateGridGraph
from fibheap import Fheap
import math
import heapq

def calculate_f(current_distance, edge: Edge, weighted: bool, end):
    g = current_distance + edge._weight
    if weighted:
        h = edge._dst.calculate_distance(end)
        
        # Uncomment the following line if using grid world
        # h = abs(end._x - edge._dst._x) + abs(end._y - edge._dst._y)
        
        return g + h, h
    else:
        return g, 1

def a_star(graph: Graph, start: Node, end: Node, weighted: bool = True):
    i = 0
    # Create a priority queue of edges to consider
    pq = []
    heapq.heappush(pq, (0, 0, Edge(src=None, dst=start, weighted=False)))

    # Keep track of each node's previous node
    prev = [None] * graph.get_num_nodes()
    distances = [float('inf')] * graph.get_num_nodes()
    f_score = [float('inf')] * graph.get_num_nodes()
    distances[start._index] = 0

    # Keep track of the order in which edges are added and considered
    added_edges = []
    considered_edges = []

    # Repeatedly pop from priority queue
    while pq:
        # Get the next edge in the pqueue
        f, h, current_edge = heapq.heappop(pq)

        # Get the 2 nodes of the edge
        previous = current_edge._src
        current = current_edge._dst

        # Only consider nodes which have not previously been reached
        if (prev[current._index] == None):
            # New edge has been added
            added_edges.append(current_edge)

            # Set parent and distance
            if current is not start:
                prev[current._index] = previous._index
                distances[current._index] = distances[previous._index] + current_edge._weight

            if current is end:
                return distances, prev, added_edges, considered_edges

            # Get all of the adjacent edges
            adjacent_edges = current.get_edges()

            # Keep track of which edges were considered
            considered = []

            # Check every adjacent edge
            for adjacent_edge in adjacent_edges:
                # Get the weight and the node
                weight = adjacent_edge._weight
                prospect = adjacent_edge._dst

                
                f, h = calculate_f(distances[current._index], adjacent_edge, weighted, end)

                # If the distance is less than the current distance for that node, keep track of it
                if f_score[prospect._index] > f:
                    considered.append(adjacent_edge)
                    f_score[prospect._index] = f

                    heapq.heappush(pq, (f_score[prospect._index], h, adjacent_edge))

            considered_edges.append(considered)

    return distances, prev, added_edges, considered_edges
