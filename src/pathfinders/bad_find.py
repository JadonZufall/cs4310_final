from src.obj.graph import Graph
from src.obj.graph import Node
import itertools


def _get_weight(nodes: list[Node], combo: list[int]) -> int:
    weight = 0
    for i, nidx in enumerate(combo):
        if i == len(combo) - 1: break
        weight += nodes[nidx].calculate_distance(nodes[combo[i]])
    return weight

def remap_combos(valid_combos, start, end) -> list[list[int]]:
    result = []
    for p in valid_combos:
        if p[0] != start:
            continue
        while p[-1] != end and len(p) != 1:
            p.pop(-1)
        if len(p) == 1:
            continue
        result.append(p)
    return result

def bad_find(graph: Graph, start: Node, end: Node):
    nodes = graph.get_nodes()
    combos = itertools.combinations(range(len(nodes)), len(nodes))
    combos = [list(i) for i in combos]
    valid_combos = []
    for c in combos:
        for i, nidx in enumerate(c):
            if i == len(c) - 1:
                continue
            if nodes[nidx+1] not in nodes[nidx].get_neighbors():
                break
        else:
            valid_combos.append(c)
    
    valid_combos = remap_combos(valid_combos, nodes.index(start), nodes.index(end))
    weights = [_get_weight(nodes, i) for i in valid_combos]
    if len(weights) == 0: return -1
    min_w = min(weights)
    shortest_path = valid_combos[weights.index(min(weights))]
        
    
    
    
    
    