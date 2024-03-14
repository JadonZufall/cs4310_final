from typing import Optional

class Node:
    def __init__(self, value: Optional[str]=None) -> None:
        self._value: Optional[str] = value
