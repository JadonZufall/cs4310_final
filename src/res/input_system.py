from typing import Optional
import pygame
from src.res.event_system import EventHandler, EventListener
from src.res.context import Context, _Context


class MouseInputBounds:
    x: int
    y: int
    on_hover: Optional[callable]
    on_click: Optional[callable]
    is_enabled: bool
    
    mouse_motion_listener: Optional[EventListener]
    mouse_click_listener: Optional[EventListener]
    def __init__(self, x: int, y: int, on_hover: Optional[callable]=None, on_click: Optional[callable]=None) -> None:
        self.is_enabled = True
        self.x = x
        self.y = y
        self.on_hover = on_hover
        self.on_click = on_click
        if self.on_hover is not None:
            self.mouse_motion_listener = EventHandler.bind_to_event(pygame.MOUSEMOTION, self.mouse_motion_event)
        if self.on_click is not None:
            self.mouse_click_listener = EventHandler.bind_to_event(pygame.MOUSEBUTTONDOWN, self.mouse_click_event)
    
    def destroy(self) -> None:
        if self.mouse_click_listener is not None:
            self.mouse_click_listener.destory()
        if self.mouse_motion_listener is not None:
            self.mouse_motion_listener.destory()
        self.is_enabled = False
    
    def in_bounds(x: int, y: int) -> bool:
        raise NotImplementedError
        
    def mouse_click_event(self, dt: int, event: pygame.event.Event):
        # TODO: Only call on mouse1 / seperate events.
        if not self.is_enabled:
            return False
        mx, my = pygame.mouse.get_pos()
        if self.in_bounds(mx, my):
            self.on_click(dt, event)
    
    def mouse_motion_event(self, dt: int, event: pygame.event.Event):
        if not self.is_enabled:
            return False
        mx, my = pygame.mouse.get_pos()
        if self.in_bounds(mx, my):
            self.on_hover(dt, event)
    
    def enable(self) -> None: 
        if self.mouse_click_listener is not None:
            self.mouse_click_listener.enable()
        if self.mouse_motion_listener is not None:
            self.mouse_motion_listener.enable()
        self.is_enabled = True
        
    def disable(self) -> None: 
        if self.mouse_click_listener is not None:
            self.mouse_click_listener.disable()
        if self.mouse_motion_listener is not None:
            self.mouse_motion_listener.disable()
        self.is_enabled = False

class MouseInputBoundsCircle(MouseInputBounds):
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
        
class MouseInputBoundsRect(MouseInputBounds):
    def __init__(self, x: int, y: int, w: int, h: int, on_hover: Optional[callable]=None, on_click: Optional[callable]=None) -> None:
        super().__init__(x, y, on_click=on_click, on_hover=on_hover)
        self.w: int = w
        self.h: int = h
    
    def in_bounds(self, x: int, y: int) -> bool:
        if self.x > x or self.y > y or self.x + self.w < x or self.y + self.h < y:
            return False
        return True


class _MouseInputHandler:
    input_bounds: list[MouseInputBounds] 
    def __init__(self) -> None:
        self.input_bounds = list()

class _KeyboardInputHandler:
    def __init__(self) -> None:
        pass


MouseInputHandler = _MouseInputHandler()
KeyboardInputHandler = _KeyboardInputHandler()
