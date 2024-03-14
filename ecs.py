import pygame
pygame.init()

ColorType = tuple[int, int, int]

class Context:
    def __init__(self) -> None:
        self._is_running: bool = True
        self._state: State = None
        self._fps_cap: int = 60
    
    def set_state(self, state: "State") -> None:
        self._state: State = state
    
    def stop(self) -> None:
        self._is_running: bool = False
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @property
    def state(self) -> "State":
        return self._state
    
    @property
    def fps_cap(self) -> int:
        return self._fps_cap

class Container:
    def __init__(self) -> None:
        pass


class Position:
    def __init__(self, x: int, y: int) -> None:
        self._x: int = x
        self._y: int = y
    
    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self) -> tuple[int, int]:
        return self._x, self._y

class Size:
    def __init__(self, w: int, h: int) -> None:
        self._w: int = w
        self._h: int = h
    
    @property
    def w(self) -> int:
        return self._w
    
    @property
    def h(self) -> int:
        return self._h
    
    @property
    def size(self) -> tuple[int, int]:
        return self.w, self.h

class ZLevel:
    def __init__(self, z_index: int) -> None:
        self._z_index: int = z_index

class Frame(Container, Position, Size, ZLevel):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], z_index: int=0) -> None:
        super().__init__()
        Position.__init__(self, x=pos[0], y=pos[1])
        Size.__init__(self, w=size[0], h=size[1])
        ZLevel.__init__(self, z_index=z_index)
    
    def handle_event(self, event: pygame.Event, dt: int) -> None:
        pass
    
    def handle_render(self, surface: pygame.Surface, dt: int) -> None:
        pass

class Cell(Container, Position):
    def __init__(self, pos: tuple[int, int], initial_value: int=0) -> None:
        super().__init__()
        Position.__init__(self, x=pos[0], y=pos[1])
        self._value: int = initial_value
    
    def handle_event(self, event: pygame.Event, dt: int) -> None:
        pass
    
    def handle_render(self, surface: pygame.Surface, dt: int) -> None:
        pass

class Grid(Container, Size):
    def __init__(self, size: tuple[int, int], initial_value: int=0) -> None:
        super().__init__()
        Size.__init__(self, w=size[0], h=size[1])
        self._data: list[list[Cell]] = list()
        for i in range(0, self.h):
            self._data.append(list())
            for j in range(0, self.w):
                self._data[i].append(Cell(pos=(i, j), initial_value=initial_value))
    
    def handle_event(self, event: pygame.Event, dt: int) -> None:
        pass
    
    def propagate_render(self, surface: pygame.Surface, dt: int) -> None:
        for i in range(0, self.h):
            for j in range(0, self.w):
                self._data[i][j].handle_render(surface=surface, dt=dt)
    
    def handle_render(self, surface: pygame.Surface, dt: int) -> None:
        src: pygame.Surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        self.propagate_render(surface=src, dt=dt)
        surface.blit(src, (0, 0))
        


class GridFrame(Frame):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], grid_size: tuple[int, int], z_index: int=0, initial_value: int=0) -> None:
        super().__init__(pos=pos, size=size, z_index=z_index)
        self._grid: Grid = Grid(size=grid_size, initial_value=initial_value)
    
    def handle_event(self, event: pygame.Event, dt: int) -> None:
        self._grid.handle_event(event=event, dt=dt)
    
    def handle_render(self, surface: pygame.Surface, dt: int) -> None:
        src: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._grid.handle_render(surface=src, dt=dt)
        surface.blit(src, self.pos)

class State:
    def __init__(self, context: Context, window: pygame.Surface, clock: pygame.time.Clock) -> None:
        self._context: Context = context
        self._window: pygame.Surface = window
        self._clock: pygame.time.Clock = clock
        self._frames: list[Frame] = list()
        self._bg: ColorType = (0, 0, 0)
    
    def append_frame(self, frame: Frame) -> None:
        self._frames.append(frame)
    
    def propagate_event(self, event: pygame.Event, dt: int) -> None:
        for instance in self._frames:
            instance.handle_event(event=event, dt=dt)
    
    def propagate_render(self, surface: pygame.Surface, dt: int) -> None:
        for instance in self._frames:
            instance.handle_render(surface=surface, dt=dt)
    
    def loop(self) -> None:
        dt: int = self._clock.tick(self._context.fps_cap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._context.stop()
            else:
                self.propagate_event(event=event, dt=dt)
        self._window.fill(self._bg)
        self.propagate_render(surface=self._window, dt=dt)
        pygame.display.flip()
    

def main() -> None:
    context: Context = Context()
    window: pygame.Surface = pygame.display.set_mode((500, 500))
    clock: pygame.time.Clock = pygame.time.Clock()
    initial_state: State = State(window=window, clock=clock)
    while context.is_running:
        context.state.loop()


if __name__ == "__main__":
    main()
