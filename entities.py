from dataclasses import dataclass
from typing import Optional

@dataclass
class Entity:
    x: float
    y: float
    width: int
    height: int
    velocity_x: float = 0
    velocity_y: float = 0
    dead: bool = False

@dataclass
class Star:
    x: float
    y: float
    speed: float
    color: tuple[int, int, int]