

class _Context:
    scale_x: float
    scale_y: float
    offset_x: int
    offset_y: int
    
    def __init__(self) -> None:
        self.scale_x = 0.0
        self.scale_y = 0.0
        self.offset_x = 0
        self.offset_y = 0

Context = _Context()