import pygame
pygame.init()

WINDOW_WIDTH: int = 500
WINDOW_HEIGHT: int = 500
window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock: pygame.time.Clock = pygame.time.Clock()

context_instances: list["Context"] = list()
class Context:
    def __init__(self, window: pygame.Surface, clock: pygame.time.Clock) -> None:
        self._window = window
        self._clock = clock
        self._width: int = window.get_width()
        self._height: int = window.get_height()
        self._frames: list[Frame] = list()
        self._is_active: bool = False
        context_instances.append(self)
    
    def deactivate(self) -> bool:
        if not self._is_active:
            return False
        self._is_active: bool = False
        return True
    
    def activate(self) -> bool:
        if self._is_active:
            return False
        # Deactivate all other Context instances, only one may be active at a time.
        for instance in context_instances:
            instance.deactivate()
        self._is_active: bool = True
        return True
    
    def attach(self, frame: "Frame", sort: bool=True) -> None:
        self._frames.append(frame)
        if sort:
            self.sort_frames()
    
    def sort_frames(self) -> None:
        self._frames.sort(key=lambda x: x._z_index)
    
    def on_click(self, mouse_x: int, mouse_y: int) -> None:
        for frame_instance in self._frames:
            pass
        

class Frame:
    def __init__(self, window: pygame.Surface, width: int, height: int, x_offset: int, y_offset: int, z_index: int) -> None:
        self._window: pygame.Surface = window
        self._surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._width: int = width
        self._height: int = height
        self._x_offset: int = x_offset
        self._y_offset: int = y_offset
        self._z_index: int = z_index
        self._is_active: bool = True
    
    def render(self) -> None:
        pass


        