import unittest
from src.obj.graph import Graph
from src.obj.node import Node
from src.tests.graph_generator import generate_complete_graph, generate_random_graph, generate_tree_graph
from src.pathfinders.dijkstra import dijkstra
from src.pathfinders.a_star import a_star

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

class TestPathfinding(unittest.TestCase):
    def check_dijkstra_end(self, graph: Graph, all_pairs_shortest):
        # Get the nodes from the graph
        nodes = graph.get_nodes()

        for node1 in nodes:
            for node2 in nodes:
                dist, prev, edges, considered = dijkstra(graph, node1, node2)
                self.assertAlmostEqual(all_pairs_shortest[node1._index][node2._index], dist[node2._index], places=4, msg="A* Failure")

    def check_dijkstra(self, graph: Graph, all_pairs_shortest):
        # Get the nodes from the graph
        nodes = graph.get_nodes()

        for node in nodes:
            dist, prev, edges, considered = dijkstra(graph, node)

            for i in range(len(nodes)):
                self.assertAlmostEqual(all_pairs_shortest[node._index][i], dist[i],places=4, msg="Dijstra Failure")

    def check_a_star(self, graph: Graph, all_pairs_shortest, weighted):
        # Get the nodes from the graph
        nodes = graph.get_nodes()

        for node1 in nodes:
            for node2 in nodes:
                dist, prev, edges, considered = a_star(graph, node1, node2, weighted)
                self.assertAlmostEqual(all_pairs_shortest[node1._index][node2._index], dist[node2._index], places=4, msg="A* Failure")

    def all_pathfinders(self, graph: Graph, weighted):
        # Get all Pairs Shortest Path for the Graph
        all_pairs_shortest = floyd_warshall(graph)

        # Test each pathfindeer
        self.check_dijkstra(graph, all_pairs_shortest)
        self.check_a_star(graph, all_pairs_shortest, weighted)

    def testSmallTree(self):
        graph1 = generate_tree_graph(num_nodes=5, weighted=False, directed=False)
        graph2 = generate_tree_graph(num_nodes=5, weighted=False, directed=True)
        graph3 = generate_tree_graph(num_nodes=5, weighted=True, directed=False)
        graph4 = generate_tree_graph(num_nodes=5, weighted=True, directed=True)

        self.all_pathfinders(graph1, False)
        self.all_pathfinders(graph2, False)
        self.all_pathfinders(graph3, True)
        self.all_pathfinders(graph4, True)

    def testSmallRandom(self):
        graph1 = generate_random_graph(num_nodes=5, weighted=False, directed=False)
        graph2 = generate_random_graph(num_nodes=5, weighted=False, directed=True)
        graph3 = generate_random_graph(num_nodes=5, weighted=True, directed=False)
        graph4 = generate_random_graph(num_nodes=5, weighted=True, directed=True)

        self.all_pathfinders(graph1, False)
        self.all_pathfinders(graph2, False)
        self.all_pathfinders(graph3, True)
        self.all_pathfinders(graph4, True)

    def testSmallComplete(self):
        graph1 = generate_complete_graph(num_nodes=5, weighted=False, directed=False)
        graph2 = generate_complete_graph(num_nodes=5, weighted=False, directed=True)
        graph3 = generate_complete_graph(num_nodes=5, weighted=True, directed=False)
        graph4 = generate_complete_graph(num_nodes=5, weighted=True, directed=True)

        self.all_pathfinders(graph1, False)
        self.all_pathfinders(graph2, False)
        self.all_pathfinders(graph3, True)
        self.all_pathfinders(graph4, True)

    def testMedTree(self):
        graph1 = generate_tree_graph(num_nodes=50, weighted=False, directed=False)
        graph2 = generate_tree_graph(num_nodes=50, weighted=False, directed=True)
        graph3 = generate_tree_graph(num_nodes=50, weighted=True, directed=False)
        graph4 = generate_tree_graph(num_nodes=50, weighted=True, directed=True)

        self.all_pathfinders(graph1, False)
        self.all_pathfinders(graph2, False)
        self.all_pathfinders(graph3, True)
        self.all_pathfinders(graph4, True)

    def testMedRandom(self):
        graph1 = generate_random_graph(num_nodes=50, weighted=False, directed=False)
        graph2 = generate_random_graph(num_nodes=50, weighted=False, directed=True)
        graph3 = generate_random_graph(num_nodes=50, weighted=True, directed=False)
        graph4 = generate_random_graph(num_nodes=50, weighted=True, directed=True)

        self.all_pathfinders(graph1, False)
        self.all_pathfinders(graph2, False)
        self.all_pathfinders(graph3, True)
        self.all_pathfinders(graph4, True)
    
    def testMedComplete(self):
        graph1 = generate_complete_graph(num_nodes=50, weighted=False, directed=False)
        graph2 = generate_complete_graph(num_nodes=50, weighted=False, directed=True)
        graph3 = generate_complete_graph(num_nodes=50, weighted=True, directed=False)
        graph4 = generate_complete_graph(num_nodes=50, weighted=True, directed=True)

        self.all_pathfinders(graph1, False)
        self.all_pathfinders(graph2, False)
        self.all_pathfinders(graph3, True)
        self.all_pathfinders(graph4, True)

if __name__ == "__main__":
    unittest.main()