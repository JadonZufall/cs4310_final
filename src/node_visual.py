import pygame

# Type Hints
ColorType = tuple[int, int, int]

# Const
TAB = "    "
WHITE: ColorType = (255, 255, 255)
BLACK: ColorType = (0, 0, 0)
RED: ColorType = (255, 0, 0)
GREEN: ColorType = (0, 255, 0)
BLUE: ColorType = (0, 0, 255)
CYAN: ColorType = (0, 255, 255)


# Config
WINDOW_WIDTH: int = 500
WINDOW_HEIGHT: int = 500
FRAMERATE_CAP: int = 60

# Style
WINDOW_BG: ColorType = WHITE

# Globals
is_running: bool = True
window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, vsync=1)
clock: pygame.time.Clock = pygame.time.Clock()
font: pygame.font.Font = pygame.font.SysFont("ComicSans", 12)


class Vertex:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._edges: list[Edge] = []
    
    def connect(self, other: "Vertex", weight: float) -> "Edge":
        result: Edge = Edge(a=self, b=other, weight=weight)
        self._edges.append(result)
        return result


class Edge:
    def __init__(self, a: Vertex, b: Vertex, weight: float) -> None:
        self._a: Vertex = a
        self._b: Vertex = b
        self._weight: float = weight



notifications: list["Notification"] = []
class Notification:
    def __init__(self, msg: str, timeout: int=1000, bg: ColorType=GREEN, fg: ColorType=BLACK) -> None:
        self.msg: str = msg
        self.timeout: int = timeout
        self.fg: ColorType = fg
        self.bg: ColorType = bg
        self.img: pygame.Surface = pygame.Surface((150, 20))
        self.img.fill(bg)
        txt: pygame.Surface = font.render(self.msg, True, fg)
        tx: int = (self.img.get_width() - txt.get_width()) // 2
        ty: int = (self.img.get_height() - txt.get_height()) // 2
        self.img.blit(txt, (tx, ty))
    
    def draw(self, surface: pygame.Surface) -> None:
        x: int = surface.get_width() - self.img.get_width()
        y: int = 0
        surface.blit(surface, (x, y))
    
    def update(self, delta: int) -> None:
        self.timeout -= delta
        if self.timeout <= 0:
            notifications.remove(self)

def display_notifications(surface: pygame.Surface, delta: int) -> None:
    for i, v in enumerate(notifications):
        v.update(delta)
        v.draw(surface=surface)


def command_pallet() -> None:
    pass

def quit() -> None:
    global is_running
    is_running = False

def main() -> None:
    while is_running:
        delta = clock.tick(FRAMERATE_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        window.fill(WHITE)
        display_notifications(surface=window, delta=delta)
        
        pygame.display.flip()
            
        


if __name__ == "__main__":
    main()


