import pygame

class EventListener:
    parent: "_EventHandler"
    event_type: int
    func: callable
    args: list[any]
    kwargs: dict[str, any]
    is_enabled: bool
    
    def __init__(self, parent: "_EventHandler", event_type: int, func: callable, args: list[any]=[], kwargs: dict[str, any]=dict()) -> None:
        self.parent = parent
        self.event_type = event_type
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_enabled = True
    
    def destroy(self) -> None:
        index = self.parent.listeners[self.event_type].index(self)
        self.parent.listeners[self.event_type].pop(index)
    
    def trigger(self, dt: int, event: pygame.event.Event) -> None:
        if self.is_enabled:
            self.func(dt, event, *self.args, **self.kwargs)
    
    def disable(self) -> None:
        self.is_enabled = False
    
    def enable(self) -> None:
        self.is_enabled = True
    

class _EventHandler:
    listeners: dict[str, list[EventListener]]
    
    def __init__(self) -> None:
        self.listeners = dict()
    
    def update(self, dt: int) -> None:
        for event in pygame.event.get():
            for listener in self.listeners.get(event.type, list()):
                listener.trigger(dt, event)
    
    def bind_to_event(self, event_type: int, func: callable, args: list[any]=[], kwargs: dict[str, any]=dict()) -> EventListener:
        self.listeners.setdefault(event_type, list())
        event_functions: list[EventListener] = self.listeners.get(event_type, None)
        listener = EventListener(self, event_type, func, args=args, kwargs=kwargs)
        event_functions.append(listener)
        return listener


EventHandler = _EventHandler()