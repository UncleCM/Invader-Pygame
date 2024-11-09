from typing import Type
from gyro_controller import GyroController
from button_controller import ButtonController
from constants import Entity, SHOOT_COOLDOWN, BULLET_SPEED, PLAYER_SPEED
import pygame

def add_controls(game_class: Type) -> Type:
    """
    Decorator to add gyroscope and button controls to the game class.
    
    Args:
        game_class: The original game class to modify
        
    Returns:
        Modified game class with gyroscope and button support
    """
    original_init = game_class.__init__
    
    def new_init(self):
        original_init(self)
        # Initialize controllers
        try:
            self.gyro = GyroController()
            self.using_gyro = True
            print("Gyroscope initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize gyroscope: {e}")
            print("Falling back to keyboard controls")
            self.using_gyro = False
            
        try:
            self.button = ButtonController()
            self.using_button = True
            self.last_button_state = False
            print("Button controller initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize button: {e}")
            print("Falling back to keyboard controls for shooting")
            self.using_button = False
    
    original_handle_input = game_class.handle_input
    
    def new_handle_input(self):
        # Handle movement - try gyro first, fall back to keyboard
        if hasattr(self, 'using_gyro') and self.using_gyro:
            try:
                self.player.velocity_x = self.gyro.get_rotation(PLAYER_SPEED)
            except Exception as e:
                print(f"Error reading gyroscope: {e}")
                self.using_gyro = False
                # Fall back to keyboard controls for this frame
                original_handle_input(self)
        else:
            # Use keyboard controls if no gyro
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.velocity_x = -PLAYER_SPEED
            elif keys[pygame.K_d]:
                self.player.velocity_x = PLAYER_SPEED
            else:
                self.player.velocity_x = 0
        
        # Handle shooting - try button first, fall back to keyboard
        if hasattr(self, 'using_button') and self.using_button:
            try:
                current_button_state = self.button.is_pressed()
                
                # Shoot only on button press (not hold)
                if current_button_state and not self.last_button_state and self.shoot_timer <= 0:
                    self.shoot_timer = SHOOT_COOLDOWN
                    bullet = Entity(
                        self.player.x + self.player.width // 2 - self.bullet_img.get_width() // 2,
                        self.player.y,
                        self.bullet_img.get_width(),
                        self.bullet_img.get_height(),
                        0,
                        -BULLET_SPEED
                    )
                    self.bullets.append(bullet)
                
                self.last_button_state = current_button_state
            except Exception as e:
                print(f"Error reading button: {e}")
                self.using_button = False
                # Fall back to keyboard controls for this frame
                if pygame.key.get_pressed()[pygame.K_SPACE] and self.shoot_timer <= 0:
                    self.shoot_timer = SHOOT_COOLDOWN
                    bullet = Entity(
                        self.player.x + self.player.width // 2 - self.bullet_img.get_width() // 2,
                        self.player.y,
                        self.bullet_img.get_width(),
                        self.bullet_img.get_height(),
                        0,
                        -BULLET_SPEED
                    )
                    self.bullets.append(bullet)
        else:
            # Use keyboard controls if no button
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.shoot_timer <= 0:
                self.shoot_timer = SHOOT_COOLDOWN
                bullet = Entity(
                    self.player.x + self.player.width // 2 - self.bullet_img.get_width() // 2,
                    self.player.y,
                    self.bullet_img.get_width(),
                    self.bullet_img.get_height(),
                    0,
                    -BULLET_SPEED
                )
                self.bullets.append(bullet)
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if hasattr(self, 'using_button') and self.using_button:
            try:
                self.button.cleanup()
            except:
                pass  # Ignore cleanup errors
    
    game_class.__init__ = new_init
    game_class.handle_input = new_handle_input
    game_class.cleanup = cleanup
    
    return game_class