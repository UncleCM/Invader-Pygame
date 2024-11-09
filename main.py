import pygame
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 200
BULLET_SPEED = 400
ALIEN_SPEED = 50
SHOOT_COOLDOWN = 0.1
ALIEN_SHOOT_COOLDOWN = 6.0
SHOOT_CHANCE = 0.005
COLLISION_RADIUS = 24
ALIEN_PROJECTILE_SPEED = 150

# Background constants
NUM_STARS = 200
STAR_SPEEDS = [50, 100, 150]
STAR_COLORS = [(100, 100, 100), (150, 150, 150), (255, 255, 255)]

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Sprite scale factors
PLAYER_ALIEN_SCALE = 2.0
BULLET_SCALE = 3.0  # Increased from default
ALIEN_PROJECTILE_SCALE = 3.0  # Increased from default

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
    color: Tuple[int, int, int]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        
        # Load assets
        self.player_img = pygame.image.load("assets/player.png")
        self.alien_img = pygame.image.load("assets/alien.png")
        self.bullet_img = pygame.image.load("assets/bullet.png")
        self.alien_projectile_img = pygame.image.load("assets/alien_projectile.png")
        
        # Scale images
        self.player_img = pygame.transform.scale(self.player_img, 
            (int(self.player_img.get_width() * PLAYER_ALIEN_SCALE), 
             int(self.player_img.get_height() * PLAYER_ALIEN_SCALE)))
             
        self.alien_img = pygame.transform.scale(self.alien_img,
            (int(self.alien_img.get_width() * PLAYER_ALIEN_SCALE),
             int(self.alien_img.get_height() * PLAYER_ALIEN_SCALE)))
             
        self.bullet_img = pygame.transform.scale(self.bullet_img,
            (int(self.bullet_img.get_width() * BULLET_SCALE),
             int(self.bullet_img.get_height() * BULLET_SCALE)))
             
        self.alien_projectile_img = pygame.transform.scale(self.alien_projectile_img,
            (int(self.alien_projectile_img.get_width() * ALIEN_PROJECTILE_SCALE),
             int(self.alien_projectile_img.get_height() * ALIEN_PROJECTILE_SCALE)))
        
        # Initialize stars
        self.stars = self.create_stars()
        
        # Game state
        self.reset_game()
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        
    def create_stars(self) -> List[Star]:
        stars = []
        for _ in range(NUM_STARS):
            speed_index = random.randint(0, len(STAR_SPEEDS) - 1)
            stars.append(Star(
                x=random.randint(0, WINDOW_WIDTH),
                y=random.randint(0, WINDOW_HEIGHT),
                speed=STAR_SPEEDS[speed_index],
                color=STAR_COLORS[speed_index]
            ))
        return stars
        
    def update_stars(self):
        for star in self.stars:
            star.y += star.speed * self.delta_time
            if star.y > WINDOW_HEIGHT:
                star.y = 0
                star.x = random.randint(0, WINDOW_WIDTH)
                
    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, star.color, (int(star.x), int(star.y)), 1)
            
    def reset_game(self):
        # Initialize player at the bottom center of the screen
        self.player = Entity(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - self.player_img.get_height(),
            self.player_img.get_width(),
            self.player_img.get_height()
        )
        self.aliens: List[Entity] = []
        self.bullets: List[Entity] = []
        self.alien_projectiles: List[Entity] = []
        self.shoot_timer = 0
        self.score = 0
        self.game_over = False
        self.spawn_aliens()
        
    def spawn_aliens(self):
        self.aliens.clear()
        
        base_count = 10
        extra_aliens = random.randint(1, 5)
        total_aliens = base_count + extra_aliens
        
        for _ in range(total_aliens):
            x = random.uniform(WINDOW_WIDTH * 0.1, WINDOW_WIDTH * 0.9)
            y = random.uniform(WINDOW_HEIGHT * 0.1, WINDOW_HEIGHT * 0.4)
            velocity_x = random.uniform(-30, 30)
            velocity_y = random.uniform(-20, 20)
            
            alien = Entity(
                x, y,
                self.alien_img.get_width(),
                self.alien_img.get_height(),
                velocity_x,
                velocity_y
            )
            self.aliens.append(alien)
            
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Player movement
        if keys[pygame.K_a]:
            self.player.velocity_x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.player.velocity_x = PLAYER_SPEED
        else:
            self.player.velocity_x = 0
            
        # Shooting
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot_timer = SHOOT_COOLDOWN
            # Spawn bullet from center of player
            bullet = Entity(
                self.player.x + self.player.width // 2 - self.bullet_img.get_width() // 2,
                self.player.y,
                self.bullet_img.get_width(),
                self.bullet_img.get_height(),
                0,
                -BULLET_SPEED
            )
            self.bullets.append(bullet)
            
    def update(self):
        self.delta_time = self.clock.tick(60) / 1000.0
        
        # Update stars regardless of game state
        self.update_stars()
        
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset_game()
            return
            
        # Update timers
        self.shoot_timer -= self.delta_time
        
        # Update player position
        self.player.x += self.player.velocity_x * self.delta_time
        # Keep player within screen bounds
        self.player.x = max(0, min(WINDOW_WIDTH - self.player.width, self.player.x))
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.y += bullet.velocity_y * self.delta_time
            if bullet.y < 0:
                self.bullets.remove(bullet)
                
        # Update alien projectiles
        for proj in self.alien_projectiles[:]:
            proj.y += ALIEN_PROJECTILE_SPEED * self.delta_time
            if proj.y > WINDOW_HEIGHT:
                self.alien_projectiles.remove(proj)
                
            if self.check_collision(proj, self.player):
                self.game_over = True
                
        # Update aliens
        for alien in self.aliens[:]:
            # Calculate direction to player's center
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            alien_center_x = alien.x + alien.width // 2
            alien_center_y = alien.y + alien.height // 2
            
            dx = player_center_x - alien_center_x
            dy = player_center_y - alien_center_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > 0:
                alien.velocity_x = (dx / distance) * ALIEN_SPEED
                alien.velocity_y = (dy / distance) * ALIEN_SPEED
                
            alien.x += alien.velocity_x * self.delta_time
            alien.y += alien.velocity_y * self.delta_time
            
            if (alien.x < 0 or alien.x > WINDOW_WIDTH or
                alien.y < 0 or alien.y > WINDOW_HEIGHT):
                self.aliens.remove(alien)
                continue
                
            if random.random() < SHOOT_CHANCE:
                projectile = Entity(
                    alien.x + alien.width // 2 - self.alien_projectile_img.get_width() // 2,
                    alien.y + alien.height,
                    self.alien_projectile_img.get_width(),
                    self.alien_projectile_img.get_height(),
                    0,
                    0
                )
                self.alien_projectiles.append(projectile)
                
            if self.check_collision(alien, self.player):
                self.game_over = True
                
        # Check bullet collisions with aliens
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if self.check_collision(bullet, alien):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if alien in self.aliens:
                        self.aliens.remove(alien)
                        self.score += 1
                        break
                        
        if not self.aliens:
            self.spawn_aliens()
            
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        # Calculate centers of entities
        center1_x = entity1.x + entity1.width // 2
        center1_y = entity1.y + entity1.height // 2
        center2_x = entity2.x + entity2.width // 2
        center2_y = entity2.y + entity2.height // 2
        
        dx = center1_x - center2_x
        dy = center1_y - center2_y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < COLLISION_RADIUS
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw stars first (background)
        self.draw_stars()
        
        # Draw player
        self.screen.blit(self.player_img, (self.player.x, self.player.y))
        
        # Draw aliens
        for alien in self.aliens:
            self.screen.blit(self.alien_img, (alien.x, alien.y))
        
        # Draw bullets
        for bullet in self.bullets:
            self.screen.blit(self.bullet_img, (bullet.x, bullet.y))
        
        # Draw alien projectiles
        for proj in self.alien_projectiles:
            self.screen.blit(self.alien_projectile_img, (proj.x, proj.y))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render("Game Over!", True, RED)
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            
            self.screen.blit(game_over_text,
                           (WINDOW_WIDTH//2 - game_over_text.get_width()//2,
                            WINDOW_HEIGHT//2 - 50))
            self.screen.blit(restart_text,
                           (WINDOW_WIDTH//2 - restart_text.get_width()//2,
                            WINDOW_HEIGHT//2 + 50))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.handle_input()
            self.update()
            self.draw()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()