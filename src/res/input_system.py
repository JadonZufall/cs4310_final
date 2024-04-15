from typing import Optional
import pygame
from src.res.event_system import EventHandler
from src.res.context import Context, _Context


class MouseInputBounds:
    def __init__(self, x: int, y: int, on_hover: Optional[callable]=None, on_click: Optional[callable]=None) -> None:
        self.x = x
        self.y = y
        if self.on_hover is not None:
            EventHandler.bind_to_event(pygame.MOUSEMOTION, self.mouse_motion_event)
        if self.on_hover is not None:
            EventHandler.bind_to_event(pygame.MOUSEBUTTONDOWN, self.mouse_click_event)
    
    def in_bounds(x: int, y: int) -> bool:
        raise NotImplementedError
        
    def mouse_click_event(self, dt: int, event: pygame.event.Event):
        # TODO: Only call on mouse1 / seperate events.
        mx, my = pygame.mouse.get_pos()
        if self.in_bounds(mx, my):
            self.on_click(dt, event)
    
    def mouse_motion_event(self, dt: int, event: pygame.event.Event):
        mx, my = pygame.mouse.get_pos()
        if self.in_bounds(mx, my):
            self.on_hover(dt, event)

class MouseInputBoundCircle(MouseInputBounds):
    radius: int
    on_hover: Optional[callable]
    on_click: Optional[callable]
    def __init__(self, x: int, y: int, radius: int, on_hover: Optional[callable]=None, on_click: Optional[callable]=None) -> None:
        super().__init__(x, y, on_click=on_click, on_hover=on_hover)
        self.radius = radius
    
    def in_bounds(self, x: int, y: int) -> bool:
        if ((x-self.x)**2 + (y-self.y)**2)**0.5 <= self.radius:
            return True
        return False
        

    


class _MouseInputHandler:
    input_bounds: list[MouseInputBounds] 
    def __init__(self) -> None:
        self.input_bounds = list()
    


MouseInputHandler = _MouseInputHandler()