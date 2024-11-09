from dataclasses import dataclass

# Game constants
PLAYER_SPEED = 200
BULLET_SPEED = 400
SHOOT_COOLDOWN = 0.1

@dataclass
class Entity:
    x: float
    y: float
    width: int
    height: int
    velocity_x: float = 0
    velocity_y: float = 0
    dead: bool = False