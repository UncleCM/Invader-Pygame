import pygame
import math
import random
from typing import List
import config
from entities import Entity
from background import Background
from hardware_controller import HardwareController

class GameState:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        
        # Load and scale assets
        self.load_assets()
        
        # Initialize components
        self.background = Background()
        self.hardware = HardwareController()
        self.clock = pygame.time.Clock()
        self.reset_game()
        
        # Game state
        self.state = config.MENU
        self.selected_option = 0
        self.menu_options = ["Start Game", "Quit"]
        
    def load_assets(self):
        self.player_img = self.load_and_scale("assets/player.png", config.PLAYER_ALIEN_SCALE)
        self.alien_img = self.load_and_scale("assets/alien.png", config.PLAYER_ALIEN_SCALE)
        self.bullet_img = self.load_and_scale("assets/bullet.png", config.BULLET_SCALE)
        self.alien_projectile_img = self.load_and_scale(
            "assets/alien_projectile.png", 
            config.ALIEN_PROJECTILE_SCALE
        )
        
    @staticmethod
    def load_and_scale(path: str, scale: float) -> pygame.Surface:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, 
            (int(img.get_width() * scale), 
             int(img.get_height() * scale)))

    # [Rest of the game logic methods from the original GameState class]
    # Including: reset_game, spawn_aliens, update, check_collision, etc.