import numpy as np 
from matplotlib import pyplot as plt 
from src.tests.time_tester import *


def graph() -> None:
    pass


plt.title("Pathfinding Time Complexity")
plt.xlabel("Number of nodes")
plt.ylabel("Time in ms")

runs = {}
for n in range(2, 100):
    for key, value in perform_test_on_graph(number_of_runs=10, number_of_nodes=n).items():
        runs.setdefault(key, [])
        runs[key].append(sum(list(map(lambda x: x.total_time, value))) / len(value))
    print(f"Generated node {n}")
    

for key, value in runs.items():
    plt.plot([i / 1000 for i in value], label=key)
leg = plt.legend(loc="upper center")
plt.show()