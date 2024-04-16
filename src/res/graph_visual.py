import pygame
try:
    from src.obj.graph import Graph
    from src.obj.node import Node
    from src.obj.node import Edge
    from src.utils import calc_distance
    from src.utils import calc_rel_distance
except ModuleNotFoundError as error:
    raise error
    from ..obj.graph import Graph
    from ..obj.node import Node
    from ..utils import calc_distance
    from ..utils import calc_rel_distance
pygame.init()




class GraphVisual:
    def __init__(self, win_size: tuple[int, int]) -> None:
        self._win_w: int = win_size[0]
        self._win_h: int = win_size[1]
        self.window: pygame.Surface = pygame.display.set_mode(win_size)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 12, True, False)
    
    def get_nodes_screen_pos(self, nodes: list[Node], offset: tuple[int, int]=(0, 0), scale: tuple[float, float]=(1.0, 1.0)) -> tuple[int, int]:
        result: list[tuple[int, int]] = []
        shift_x: int = 0
        shift_y: int = 0
        for i, n in enumerate(nodes):
            nx, ny = n.get_coordinates()
            nx = (((nx - offset[0]) + (.25 * self._win_w)) * scale[0]) + shift_x
            ny = (((ny - offset[1]) + (.25 * self._win_h)) * scale[1]) + shift_y
            # Shift right if left coordinate is less the 0.
            if nx < 0:
                for j, m in enumerate(result):
                    mx, my = m[0], m[1]
                    result[j] = (mx + abs(nx) + 10, my)
                shift_x += abs(nx) + 10
                nx = abs(nx) + 10
            # Shift down if top coordinate is less then 0.
            if ny < 0:
                for j, m in enumerate(result):
                    mx, my = m[0], m[1]
                    result[j] = (mx, my + abs(ny) + 10)
                shift_y += abs(ny) + 10
                ny = abs(ny) + 10
            result.append((nx, ny))
        return result
    
    def wait(self, fps: int) -> int:
        return self.clock.tick(fps)
    
    def event(self, event: pygame.event.Event) -> None:
        pass
    
    def draw(self, graph: Graph) -> None:
        self.window.fill((255, 255, 255))
        nodes: list[Node] = graph.get_nodes()
        points: list[tuple[int, int]] = self.get_nodes_screen_pos(nodes=nodes, offset=(0, 0), scale=(0.5, 0.5))
        
        # Draw edges
        for i, np in enumerate(points):
            ni = i
            n = nodes[ni]
            edges: list[Edge] = n.get_edges()
            for j, e in enumerate(edges):
                dst: Node = e.get_destination()
                if dst is nodes[i]:
                    continue
                mi = nodes.index(dst)
                m = nodes[mi]
                mp = points[mi]
                pygame.draw.line(self.window, (255, 0, 0), np, mp)
        
        # Draw vertexs
        for i, np in enumerate(points):
            ni = i
            n = nodes[ni]
            pygame.draw.circle(self.window, (0, 0, 0), np, 10)
        
        # Draw vertex values
        for i, np in enumerate(points):
            ni = i
            n = nodes[ni]
            try:
                txt = self.font.render(n.get_value(), True, (255, 255, 255), (0, 0, 0))
            except TypeError:
                txt = self.font.render(str(ni), True, (255, 255, 255), (0, 0, 0))
            nx = np[0] - 0.5 * txt.get_width()
            ny = np[1] - 0.5 * txt.get_height()
            self.window.blit(txt, dest=(nx, ny))
            print("a")
        pygame.display.flip()
                
    
    def update(self, graph: Graph) -> None:
        self.window.fill((255, 255, 255))
        nodes: list[Node] = graph.get_nodes()
        min_nx: int = 0
        min_ny: int = 0
        max_nx: int = 0
        max_ny: int = 0
        for i, n in enumerate(nodes):
            np: list[int, int] = n.get_coordinates()
            nx: int = np[0]
            ny: int = np[1]
            min_nx = nx if nx < min_nx else min_nx
            min_ny = ny if ny < min_ny else min_ny
            max_nx = nx if nx > max_nx else max_nx
            max_ny = ny if ny > max_ny else max_ny
        add_nx: int = -1 * min_nx
        add_ny: int = -1 * min_nx
            
        d_nodes: list[tuple[float, Node, int]] = list(map(
            lambda x: (calc_rel_distance(*(0, 0), *x[1].get_coordinates()), x[1], x[0]), 
            enumerate(nodes),
        ))
        c_dist: float
        c_node: Node
        c_idx: int
        c_dist, c_node, c_idx = min(
            d_nodes,
            key=lambda x: x[0],
        )
        c_x: int
        c_y: int
        c_x, c_y = c_node.get_coordinates()
        # TODO: Rel Cords dont work atm
        min_rel_x: int = (0, None)
        min_rel_y: int = (0, None)
        max_rel_x: int = (0, None)
        max_rel_y: int = (0, None)
        for idx, n in enumerate(nodes):
            tx, ty = n.get_coordinates()
            rx, ry = tx - c_x, ty - c_y
            if rx < min_rel_x[0]:
                min_rel_x = rx, idx
            if ry < min_rel_y[0]:
                min_rel_y = ry, idx
            if rx > max_rel_x[0]:
                max_rel_x = rx, idx
            if ry > max_rel_y[0]:
                max_rel_y = ry, idx
        if None in (min_rel_x[-1], min_rel_y[-1], max_rel_x[-1], max_rel_y[-1]):
            # !WARN: This means that something went wrong, but Im not gonna worry about it.
            x_range: int = self._win_w
            y_range: int = self._win_h
            x_scale: float = 1
            y_scale: float = 1
            r_scale: float = 1
        else:
            x_range: int = max_rel_x[0] + abs(min_rel_x[0])
            y_range: int = max_rel_y[0] + abs(min_rel_y[0])
            x_scale: float = self._win_w / x_range
            y_scale: float = self._win_h / y_range
            r_scale: float = min(min(x_scale, y_scale), min(self._win_w * .1, self._win_h * .1))
        
        # TODO: Remove this
        x_scale, y_scale = 1, 1
        r_scale = 1
        
        for i, n in enumerate(nodes):
            nx: int
            ny: int
            nx, ny = n.get_coordinates()
            if nx < 0 or ny < 0:
                # !WARN: Rendering off screen
                print(f"OFFSCREEN RENDERING ({nx}, {ny})")
            nx = int(((nx - c_x) + .25*self._win_w) * x_scale)
            ny = int(((ny - c_y) + .25*self._win_h) * y_scale)
            for e in n.get_edges():
                dst = e.get_destination()
                if dst is e:
                    dst = e.get_source()
                dst_x: int
                dst_y: int
                dst_x, dst_y = dst.get_coordinates()
                dst_x = int(((dst_x - c_x) + .25*self._win_w) * x_scale)
                dst_y = int(((dst_y - c_y) + .25*self._win_h) * y_scale)
                pygame.draw.line(self.window, (255, 0, 0), (nx, ny), (dst_x, dst_y))
        
        
        for i, n in enumerate(nodes):
            nx: int
            ny: int
            nx, ny = n.get_coordinates()
            if nx < 0 or ny < 0:
                # !WARN: Rendering off screen
                print(f"OFFSCREEN RENDERING ({nx}, {ny})")
            nx = int(((nx - c_x) + .25*self._win_w) * x_scale)
            ny = int(((ny - c_y) + .25*self._win_h) * y_scale)
            pygame.draw.circle(self.window, (0, 0, 0), (nx, ny), radius=int(r_scale * 10))
        
        for i, n in enumerate(nodes):
            try:
                txt: pygame.Surface = self.font.render(n.get_value(), True, (255, 255, 255), (0, 0, 0))
            except TypeError:
                txt: pygame.Surface = self.font.render(str(i), True, (255, 255, 255), (0, 0, 0))
            nx, ny = n.get_coordinates()
            nx = int(((nx - c_x) + .25*self._win_w) * x_scale - 0.5 * txt.get_width())
            ny = int(((ny - c_y) + .25*self._win_h) * y_scale - 0.5 * txt.get_height())
            self.window.blit(txt, dest=(nx, ny))
        
        pygame.display.flip()

        
        
        
            
