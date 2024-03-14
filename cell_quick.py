
class Cell:
    def __init__(self, x: int, y: int, value: int=0) -> None:
        self._x: int = x
        self._y: int = y
        self._value: int = value
    
    def set_value(self, value: int) -> None:
        self._value: int = value

class CellMatrix:
    def __init__(self, width: int, height: int) -> None:
        self._w: int = width
        self._h: int = height
        self._data: list[list[Cell]] = [[Cell(j, i) for j in range(0, self._w)] for i in range(0, self._h)]
    
    def set_value(self, x: int, y: int, value: int) -> None:
        self._data[y][x].set_value(value=value)
    
    @staticmethod
    def serialize(instance: "CellMatrix") -> str:
        w: str = f"{instance._w:0>5}"
        h: str = f"{instance._h:0>5}"
        d0: list[list[int]] = [[instance._data[i][j]._value for j in range(0, instance._w)] for i in range(0, instance._h)]
        d1: list[str] = ["".join(d0[i]) for i in range(0, len(d0))]
        d2: str = "".join(d0)
        return f"{w}{h}{d2}"
    
    @staticmethod
    def deserialize(data: str) -> "CellMatrix":
        w: int = int(data[0:5])
        h: int = int(data[5:10])
        result: CellMatrix = CellMatrix(width=w, height=h)
        d: list[str] = [int(data[10+(i*w):15+(i*w)].split("")) for i in range(0, h)]
        
        
        