from typing import Optional
from random import randint
import pickle
import pygame
pygame.init()

# Type Hints
ColorType = tuple[int, int, int]

# Quick Constants
TAB = "    "
WHITE: ColorType = (255, 255, 255)
BLACK: ColorType = (0, 0, 0)
RED: ColorType = (255, 0, 0)
GREEN: ColorType = (0, 255, 0)
BLUE: ColorType = (0, 0, 255)
CYAN: ColorType = (0, 255, 255)

# Config Constants
FRAMERATE_CAP: int = 60
WINDOW_WIDTH: int = 500
WINDOW_HEIGHT: int = 500
WINDOW_MARGIN_X: int = 5
WINDOW_MARGIN_Y: int = 5
GRID_WIDTH: int = 10
GRID_HEIGHT: int = 10
CELL_PADDING: int = 1
CELL_PADDING_X: int = CELL_PADDING
CELL_PADDING_Y: int = CELL_PADDING
CELL_MARGIN: int = 1
CELL_MARGIN_X: int = CELL_MARGIN
CELL_MARGIN_Y: int = CELL_MARGIN
CELL_OUTER_WIDTH: int = (WINDOW_WIDTH - WINDOW_MARGIN_X * 2) // (GRID_WIDTH + 1)
CELL_OUTER_HEIGHT: int = (WINDOW_HEIGHT - WINDOW_MARGIN_Y * 2) // (GRID_HEIGHT + 1)
CELL_INNER_WIDTH: int = CELL_OUTER_WIDTH - (CELL_PADDING_X * 2 + CELL_MARGIN_X * 2)
CELL_INNER_HEIGHT: int = CELL_OUTER_HEIGHT - (CELL_PADDING_Y * 2 + CELL_MARGIN_Y * 2)

# Color Constants
WINDOW_BG: ColorType = WHITE
CELL_BG: ColorType = BLACK
CELL_BG_HIGHLIGHT: ColorType = RED
CELL_FG: ColorType = WHITE
CELL_FG_BLOCK: ColorType = BLACK

# Init Message
INTRO_MESSAGE: str = f"""
GridSize=({GRID_WIDTH}, {GRID_HEIGHT})
CellOuterSize=({CELL_OUTER_WIDTH}, {CELL_OUTER_HEIGHT})
CellInnerSize=({CELL_INNER_WIDTH}, {CELL_INNER_HEIGHT})
"""
print(INTRO_MESSAGE)

window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, vsync=1)
clock: pygame.time.Clock = pygame.time.Clock()
font: pygame.font.Font = pygame.font.SysFont("ComicSans", 12)
is_running: bool = True

class Cell:
    def __init__(self, x: int, y: int, parent: Optional["CellGrid"]=None, block: bool=False, highlight: bool=False, bg: ColorType=CELL_BG, fg: ColorType=CELL_FG, bg_highlight: ColorType=CELL_BG_HIGHLIGHT, fg_block: ColorType=CELL_FG_BLOCK) -> None:
        self._x: int = x
        self._y: int = y
        self._parent: Optional[CellGrid] = parent
        self.block: bool = block
        self.highlight: bool = highlight
        self._bg: ColorType = bg
        self._fg: ColorType = fg
        self._bg_highlight: ColorType = bg_highlight
        self._fg_block: ColorType = fg_block
    
    def __repr__(self) -> str:
        return f"Cell(x={self._x}, y={self._y}) {'{'}\n{TAB}Outer={self.get_outer_rect()}\n{TAB}Inner={self.get_inner_rect()}\n{'}'}"
    
    def clone(self, parent=None) -> "Cell":
        result: Cell = Cell(x=self._x, y=self._y, parent=parent, block=self.block, highlight=self.highlight, bg=self._bg, fg=self._fg, bg_highlight=self._bg_highlight, fg_block=self._fg_block)
        return result
    
    def draw(self, surface: pygame.Surface) -> "Cell":
        bg_color: ColorType = self._bg_highlight if self.highlight else self._bg
        fg_color: ColorType = self._fg_block if self.block else self._fg
        pygame.draw.rect(surface, bg_color, self.get_outer_rect())
        pygame.draw.rect(surface, fg_color, self.get_inner_rect())
        return self
    
    def set_flags(self, block: Optional[bool]=None, highlight: Optional[bool]=None) -> "Cell":
        if block is not None:
            self.block: bool = block
        if highlight is not None:
            self.highlight: bool = highlight
        return self
    
    def get_outer_pos(self) -> tuple[int, int]:
        out_x: int = (self._x * CELL_OUTER_WIDTH) + (self._x * (CELL_MARGIN_X * 2)) + (self._x * (CELL_PADDING_X * 2)) + WINDOW_MARGIN_X 
        out_y: int = (self._y * CELL_OUTER_HEIGHT) + ((self._y * (CELL_MARGIN_Y * 2)) + (self._y + 1 * (CELL_PADDING_Y * 2))) + WINDOW_MARGIN_Y 
        return (out_x, out_y)
    
    def get_inner_pos(self) -> tuple[int, int]:
        out_pos: tuple[int, int] = self.get_outer_pos()
        in_x: int = out_pos[0] + (CELL_PADDING_X + CELL_PADDING_X)
        in_y: int = out_pos[1] + (CELL_PADDING_Y + CELL_PADDING_Y)
        return (in_x, in_y)
    
    def get_outer_rect(self) -> list[int, int, int, int]:
        out_pos: tuple[int, int] = self.get_outer_pos()
        # return [out_pos[0], out_pos[1], out_pos[0] + CELL_OUTER_WIDTH, out_pos[1] + CELL_OUTER_HEIGHT]
        return [out_pos[0], out_pos[1], CELL_OUTER_WIDTH, CELL_OUTER_HEIGHT]
        
    
    def get_inner_rect(self) -> list[int, int, int, int]:
        in_pos: tuple[int, int] = self.get_inner_pos()
        # return [in_pos[0], in_pos[1], in_pos[0] + CELL_INNER_WIDTH, in_pos[1] + CELL_INNER_HEIGHT]
        return [in_pos[0], in_pos[1], CELL_INNER_WIDTH, CELL_INNER_HEIGHT]
    
    def set_pos(self, x: int, y: int) -> "Cell":
        self._x: int = x
        self._y: int = y
        return self
    
    def set_x(self, x: int) -> "Cell":
        self._x: int = x
        return self
        
    @property
    def x(self) -> int:
        return self._x
    
    def set_y(self, y: int) -> "Cell":
        self._y: int = y
        return self
    
    @property
    def y(self) -> int:
        return self._y

class CellGrid:
    def __init__(self, w: int, h: int, default_block: bool=False, default_highlight: bool=False, default_bg: ColorType=CELL_BG, default_fg: ColorType=CELL_FG, default_bg_highlight: ColorType=CELL_BG_HIGHLIGHT, default_fg_block: ColorType=CELL_FG_BLOCK) -> None:
        self._w: int = w
        self._h: int = h
        self._data: list[Cell] = [Cell(x=i % w, y=i // w, parent=self, block=default_block, highlight=default_highlight, bg=default_bg, fg=default_fg, bg_highlight=default_bg_highlight, fg_block=default_fg_block) for i in range(0, w * h)]
        self._block: bool = default_block
        self._highlight: bool = default_highlight
        self._bg: ColorType = default_bg
        self._fg: ColorType = default_fg
        self._bg_highlight: ColorType = default_bg_highlight
        self._fg_block: ColorType = default_fg
    
    def clone(self) -> "CellGrid":
        result: CellGrid = CellGrid(w=self._w, h=self._h, default_block=self._block, default_highlight=self._highlight, default_bg=self._bg, default_fg=self._fg, default_bg_highlight=self._bg_highlight, default_fg_block=self._fg_block)
        for i in range(0, len(self._data)):
            result._data[i] = self._data[i].clone(parent=result)
        return result
    
    def draw(self, surface: pygame.Surface) -> "CellGrid":
        for i, c in enumerate(self._data):
            c.draw(surface=surface)
        return self
    
    def get_cell(self, x: int, y: int) -> Cell:
        index: int = x + y * self._w
        if x < 0 or x > self.width:
            raise IndexError("Invalid w for CellGrid.get_cell w constrained by (0, CellGrid.width-1).")
        if y < 0 or y > self.height:
            raise IndexError("Invalid h for CellGrid.get_cell h constrained by (0, CellGrid.height).")
        if index < 0 or index >= len(self._data):
            raise IndexError("Invalid index for CellGrid.get_cell, this should not occur.")
        return self._data[index]

    def get_closest_cell_by_pos(self, x: int, y: int) -> Optional[Cell]:
        # TODO: This is bad but I was too lazy to do math
        min_dist: float = None
        found_target: Cell = None
        for i in range(0, len(self._data)):
            cel: Cell = self._data[i]
            cel_pos: tuple[int, int] = cel.get_outer_pos()
            cel_pos: tuple[float, float] = (cel_pos[0] + CELL_OUTER_WIDTH / 2, cel_pos[1] + CELL_OUTER_HEIGHT / 2)
            dist: float = ((x-cel_pos[0])**2+(y-cel_pos[1])**2)**0.5
            if min_dist is None or dist < min_dist:
                min_dist: float = dist
                found_target: Cell = cel
        return found_target
                
    
    @property
    def width(self) -> int:
        return self._w
    
    @property
    def height(self) -> int:
        return self._h


grid = CellGrid(w=GRID_WIDTH, h=GRID_HEIGHT, default_block=False)

initial_state = grid.clone()


print(grid.get_cell(0, 0))
print(grid.get_cell(1, 1))
print(grid.get_cell(grid.width-1, grid.height-1))

def on_click_cell(event: pygame.event.Event, cell: Cell, mx: int, my: int) -> None:
    cell.block = not cell.block

def on_rclick_cell(event: pygame.event.Event, cell: Cell, mx: int, my: int) -> None:
    cell.highlight = not cell.highlight

def on_click(event: pygame.event.Event) -> None:
    btn_pressed: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
    mx: int = mouse_pos[0]
    my: int = mouse_pos[1]
    if btn_pressed[0]:
        cel: Cell = grid.get_closest_cell_by_pos(x=mx, y=my)
        on_click_cell(event=event, cell=cel, mx=mx, my=my)
    elif btn_pressed[2]:
        cel: Cell = grid.get_closest_cell_by_pos(x=mx, y=my)
        on_rclick_cell(event=event, cell=cel, mx=mx, my=my) 


save_states: list[CellGrid] = []
last_state: CellGrid = grid.clone()
recording_frames: list[CellGrid] = []
is_recording: bool = False
recording_wait: int = 0
recording_frame: int = 0
is_playing: bool = False
def before_grid_change():
    global last_state
    last_state = grid.clone()
    if is_recording:
        recording_frames.append(grid.clone())


def get_file_name(prompt: str) -> None:
    is_getting_filename: bool = True
    letters = ""
    while is_getting_filename:
        dt: int = clock.tick(FRAMERATE_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_getting_filename: bool = False
                is_running: bool = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_getting_filename = False
                    return letters
                elif event.key == pygame.K_BACKSPACE:
                    letters = letters[:-1]
                else:
                    letters += event.unicode
        window.fill(WINDOW_BG)
        p1 = font.render(prompt, True, WHITE, BLACK)
        p2 = font.render(letters, True, WHITE, BLACK)
        w = p1.get_width() + p2.get_width()
        h = max([p1.get_height(), p2.get_height()])
        p1x = 0
        p2x = p1x + p1.get_width()
        p1y = h - p1.get_height()
        p2y = h - p2.get_height()
        pygame.draw.rect(window, BLACK, [0, 0, w, h])
        window.blit(p1, (p1x, p1y))
        window.blit(p2, (p2x, p2y))
        pygame.display.flip()
    return letters

while is_running:
    dt: int = clock.tick(FRAMERATE_CAP)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running: bool = False
        elif is_playing:
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            before_grid_change()
            on_click(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                before_grid_change()
                grid: CellGrid = initial_state.clone()
            elif event.key == pygame.K_c:
                save_states.append(grid.clone())
            elif event.key == pygame.K_v:
                try:
                    before_grid_change()
                    grid = save_states.pop()
                except IndexError:
                    print("No save states")
            elif event.key == pygame.K_z:
                grid = last_state
                before_grid_change()
            elif event.key == pygame.K_r:
                before_grid_change()
                is_recording = not is_recording
            elif event.key == pygame.K_p:
                is_recording = False
                is_playing = True
            elif event.key == pygame.K_s:
                #TODO: Save rec data
                fp: str = get_file_name("SAVE: ")
                if not fp.endswith(".dat"):
                    fp += ".dat"
                f = open(fp, "wb")
                print(recording_frames)
                pickle.dump(recording_frames, f)
                f.close()
            elif event.key == pygame.K_l:
                #TODO: Load rec data
                fp: str = get_file_name("LOAD: ")
                if not fp.endswith(".dat"):
                    fp += ".dat"
                try:
                    f = open(fp, "rb")
                    recording_frame = 0
                    recording_frames = pickle.load(f)
                    print(recording_frames)
                    grid = recording_frames[-1].clone()
                    f.close()
                except FileNotFoundError:
                    print("Failed to load file")
    window.fill(WINDOW_BG)
    if not is_playing:
        grid.draw(surface=window)
    else:
        recording_frames[recording_frame].draw(surface=window)
        if recording_wait == FRAMERATE_CAP:
            recording_wait = 0
            recording_frame += 1
        else:
            recording_wait += 1
        if recording_frame >= len(recording_frames):
            recording_frame = 0
            is_playing = False
            grid = recording_frames[-1].clone()
    if is_playing:
        pygame.draw.rect(window, GREEN, (WINDOW_WIDTH - 25, 25, 10, 10))
    if is_recording:
        pygame.draw.circle(window, RED, (WINDOW_WIDTH - 25, 25), 10)
    pygame.display.flip()
    