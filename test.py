import numpy as np 
from matplotlib import pyplot as plt 
from src.tests.time_tester import *


SKIP_BELLMAN = True
SKIP_FLOYD = True
SKIP_YENS = True
SKIP_A_STAR = False
SKIP_DIJKSTRA = False
plt.title("Pathfinding Time Complexity")
plt.xlabel("Number of nodes")
plt.ylabel("Time in ms")

runs = {}
for n in range(2, 100):
    for key, value in perform_test_on_graph(number_of_runs=10, number_of_nodes=n, skip_bellman=SKIP_BELLMAN, skip_floyd=SKIP_FLOYD, skip_yens=SKIP_YENS, skip_a_star=SKIP_A_STAR, skip_dijkstra=SKIP_DIJKSTRA).items():
        runs.setdefault(key, [])
        runs[key].append(sum(list(map(lambda x: x.total_time, value))) / len(value))
    print(f"Generated node {n}")
    

for key, value in runs.items():
    plt.plot([i / 1000 for i in value], label=key)
leg = plt.legend(loc="upper center")
plt.show()