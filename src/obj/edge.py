from src.obj.node import Node

class Edge:
    def __init__(self, src: "Node", dst: "Node") -> None:
        self._src: "Node" = src
        self._dst: "Node" = dst

