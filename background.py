import random
import pygame
from typing import List
import config
from entities import Star

class Background:
    def __init__(self):
        self.stars = self.create_stars()
        
    def create_stars(self) -> List[Star]:
        stars = []
        for _ in range(config.NUM_STARS):
            speed_index = random.randint(0, len(config.STAR_SPEEDS) - 1)
            stars.append(Star(
                x=random.randint(0, config.WINDOW_WIDTH),
                y=random.randint(0, config.WINDOW_HEIGHT),
                speed=config.STAR_SPEEDS[speed_index],
                color=config.STAR_COLORS[speed_index]
            ))
        return stars
        
    def update(self, delta_time: float):
        for star in self.stars:
            star.y += star.speed * delta_time
            if star.y > config.WINDOW_HEIGHT:
                star.y = 0
                star.x = random.randint(0, config.WINDOW_WIDTH)
                
    def draw(self, screen: pygame.Surface):
        for star in self.stars:
            pygame.draw.circle(screen, star.color, (int(star.x), int(star.y)), 1)
