from typing import Type
from constants import Entity, SHOOT_COOLDOWN, BULLET_SPEED, PLAYER_SPEED
import pygame

def add_controls(game_class: Type) -> Type:
    """
    Decorator to add gyroscope and button controls to the game class.
    Falls back gracefully to keyboard controls if hardware is unavailable.
    """
    original_init = game_class.__init__
    
    def new_init(self):
        original_init(self)
        self.using_gyro = False
        self.using_button = False
        
        # Try to initialize gyroscope
        try:
            from gyro_controller import GyroController
            self.gyro = GyroController()
            self.using_gyro = True
            print("Gyroscope initialized successfully!")
        except ImportError:
            print("MPU6050 module not available - using keyboard controls")
        except Exception as e:
            print(f"Failed to initialize gyroscope: {e}")
            print("Falling back to keyboard controls")
            
        # Try to initialize button
        try:
            from button_controller import ButtonController
            self.button = ButtonController()
            self.using_button = True
            self.last_button_state = False
            print("Button controller initialized successfully!")
        except ImportError:
            print("RPi.GPIO module not available - using keyboard controls for shooting")
        except Exception as e:
            print(f"Failed to initialize button: {e}")
            print("Falling back to keyboard controls for shooting")
    
    original_handle_input = game_class.handle_input
    
    def new_handle_input(self):
        # Handle movement
        if self.using_gyro:
            try:
                self.player.velocity_x = self.gyro.get_rotation(PLAYER_SPEED)
            except Exception as e:
                print(f"Error reading gyroscope: {e}")
                self.using_gyro = False
                # Fall back to keyboard controls for this frame
                self._handle_keyboard_movement()
        else:
            self._handle_keyboard_movement()
        
        # Handle shooting
        if self.using_button:
            try:
                current_button_state = self.button.is_pressed()
                if current_button_state and not self.last_button_state and self.shoot_timer <= 0:
                    self._shoot()
                self.last_button_state = current_button_state
            except Exception as e:
                print(f"Error reading button: {e}")
                self.using_button = False
                self._handle_keyboard_shooting()
        else:
            self._handle_keyboard_shooting()
    
    def _handle_keyboard_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.velocity_x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.player.velocity_x = PLAYER_SPEED
        else:
            self.player.velocity_x = 0
    
    def _handle_keyboard_shooting(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.shoot_timer <= 0:
            self._shoot()
    
    def _shoot(self):
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
                pass
        if hasattr(self, 'using_gyro') and self.using_gyro:
            try:
                self.gyro.cleanup()
            except:
                pass
    
    game_class.__init__ = new_init
    game_class.handle_input = new_handle_input
    game_class._handle_keyboard_movement = _handle_keyboard_movement
    game_class._handle_keyboard_shooting = _handle_keyboard_shooting
    game_class._shoot = _shoot
    game_class.cleanup = cleanup
    
    return game_class