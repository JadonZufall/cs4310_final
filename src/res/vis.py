import pygame

from src.obj.node import Node

class Frame:
    _width: int
    _height: int
    _surface: pygame.Surface
    
    def __init__(self, width: int, height: int) -> None:
        self._width, self._height = width, height
        self._surface = pygame.Surface((self._width, self._height))


class Window:
    _width: int
    _height: int
    _surface: pygame.Surface
    _clock: pygame.time.Clock
    _bg: tuple[int, int, int]
    _frames: list[Frame]
    _is_running: bool
    
    def __init__(self, width: int, height: int, bg: tuple[int, int, int]=(0, 0, 0)) -> None:
        self._width, self._height = width, height
        self._surface = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._bg = bg
        self._surface.fill(self._bg)
        self._frames = []
        self._is_running = True
    
    def redraw(self) -> None:
        self._surface.fill(self._bg)
        for i in range(self._frames):
            self._surface.blit(self._frames[i], (0, 0))
        
        pygame.display.flip()
        
    def _click_event(self, dt: int, event: pygame.event.Event) -> None:
        pass
    
    def event_loop(self, dt: int) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._click_event(self, dt, event)

def render_visual(visual: list[Node], size: tuple[int, int]) -> Window:
    result = Window(size[0], size[1], bg=(255, 255, 255))