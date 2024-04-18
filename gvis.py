from src.res.gvis import start, animate
from src.tests.graph_generator import generate_complete_graph, generate_random_graph
from src.pathfinders.a_star import a_star
from src.pathfinders.dijkstra import dijkstra
from src.pathfinders.floyd_warshal import floyd_warshall
from src.pathfinders.bellman_ford import bellman_ford
from src.pathfinders.yen import yen
#start()


graph = generate_random_graph(num_nodes=30)
start_node = graph.get_random_node()
end_node = graph.get_random_node()

nodes = graph.get_nodes()
nmap = {str(i): v for i, v in enumerate(nodes)}
a_distances, a_prev, a_added_edges, a_considered_edges = a_star(graph, start_node, end_node)
# print(a_added_edges)
a_data = list(map(lambda x: (str(nodes.index(x._src)), str(nodes.index(x._dst))), a_added_edges[1:]))
animate(graph, a_data, "a_star.mp4", nodes.index(start_node), nodes.index(end_node))

d_distances, d_prev, d_added_edges, d_considered_edges = dijkstra(graph, start_node, end_node)
# f_distances, f_prev, f_added_edges, f_considered_edges = floyd_warshall(graph)
# y_distances, y_paths = yen(graph, start_node, end_node, K=2)

# animate(graph, fdat, "")

# fdat = [(str(random.randint(0, 10-1)), str(random.randint(0, 10-1))) for i in range(0, 100)]
