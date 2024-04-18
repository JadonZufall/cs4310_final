import time
from src.tests.graph_generator import generate_random_graph, generate_complete_graph, generate_tree_graph
from src.pathfinders.a_star import a_star
from src.pathfinders.dijkstra import dijkstra
from src.pathfinders.bellman_ford import bellman_ford
from src.pathfinders.bad_find import bad_find
from src.pathfinders.yen import yen
from src.pathfinders.floyd_warshal import floyd_warshall

class TimeTesterResult:
    def __init__(self, func: callable, args: list[any]=[], kwargs: dict[str, any]={}) -> None:
        self.start_time: int = time.time_ns()
        self.result: any = func(*args, **kwargs)
        self.final_time: int = time.time_ns()
    
    @property
    def total_time(self) -> int:
        return self.final_time - self.start_time


class TimeTester:
    def __init__(self, names: list[str], funcs: list[callable], args: list[any]=[], kwargs: dict[str, any]={}) -> None:
        self.names: list[str] = names
        self.funcs: list[callable] = funcs
        self.args: list[any] = args
        self.kwargs: list[any] = kwargs
        self.times: list[TimeTesterResult] = [TimeTesterResult(f, args=self.args, kwargs=self.kwargs) for f in self.funcs]
    
    def rerun(self) -> dict[str, TimeTesterResult]:
        res = [(self.names[i], TimeTesterResult(f, args=self.args, kwargs=self.kwargs)) for i, f in enumerate(self.funcs)]
        funcs = {}
        for i in res:
            try:
                funcs[i[0]].append(i[1])
            except KeyError:
                funcs[i[0]] = [i[1]]

    def run_multi(self, count: int) -> dict[str, TimeTesterResult]:
        res = {}
        for i in self.names:
            res[i] = []
        for j in range(count):
            for i, n in enumerate(self.names):
                res[n].append(TimeTesterResult(self.funcs[i], args=self.args, kwargs=self.kwargs))
        return res
    

def dijkstra_wrapper(graph, start, *args, **kwargs) -> None: dijkstra(graph, start)
def floyd_warshall_wrapper(graph, *args, **kwargs) -> None: floyd_warshall(graph)
def yen_wrapper(graph, start, end, *args, **kwargs) -> None: yen(graph, start, end, len(graph.get_nodes()) // 2)

def perform_test_on_graph(number_of_runs=1, number_of_nodes=10, skip_bellman=False, skip_floyd=False, skip_yens=False, skip_dijkstra=False, skip_a_star=False) -> dict[str, list[TimeTesterResult]]:
    graph = generate_complete_graph(num_nodes=number_of_nodes, weighted=True, directed=False)
    start = graph.get_random_node()
    end = graph.get_random_node()
    
    func_names = ["a_star", "dijkstra", "yen", "floyd warshal", "bellman ford"]
    func_calls = [a_star, dijkstra_wrapper, yen_wrapper, floyd_warshall_wrapper, bellman_ford]
    if skip_bellman:
        func_names.pop(-1)
        func_calls.pop(-1)
    if skip_floyd:
        func_names.pop(3)
        func_calls.pop(3)
    if skip_yens:
        func_names.pop(2)
        func_calls.pop(2)
    if skip_a_star:
        func_names.pop(1)
        func_calls.pop(1)
    if skip_dijkstra:
        func_names.pop(0)
        func_calls.pop(0)
    result = TimeTester(
        func_names, 
        func_calls,
        args=[graph, start, end], 
        kwargs={}
    )
    return result.run_multi(number_of_runs)