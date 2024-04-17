import time
from src.tests.graph_generator import generate_random_graph, generate_complete_graph, generate_tree_graph
from src.pathfinders.a_star import a_star
from src.pathfinders.dijkstra import dijkstra
from src.pathfinders.bad_find import bad_find

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

def perform_test_on_graph(number_of_runs=1, number_of_nodes=10) -> dict[str, list[TimeTesterResult]]:
    graph = generate_complete_graph(num_nodes=number_of_nodes, weighted=True, directed=False)
    start = graph.get_random_node()
    end = graph.get_random_node()
    result = TimeTester(["a_star", "dijkstra", "bad_find"], [a_star, dijkstra_wrapper, bad_find], args=[graph, start, end], kwargs={})
    return result.run_multi(number_of_runs)