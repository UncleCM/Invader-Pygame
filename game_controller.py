from typing import Type
from gyro_controller import GyroController
from main import PLAYER_SPEED

def add_gyro_controls(game_class: Type) -> Type:
    """
    Decorator to add gyroscope controls to the game class while maintaining keyboard controls.
    
    Args:
        game_class: The original game class to modify
        
    Returns:
        Modified game class with gyroscope support
    """
    original_init = game_class.__init__
    
    def new_init(self):
        original_init(self)
        try:
            self.gyro = GyroController()
            self.using_gyro = True
            print("Gyroscope initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize gyroscope: {e}")
            print("Falling back to keyboard controls")
            self.using_gyro = False
    
    original_handle_input = game_class.handle_input
    
    def new_handle_input(self):
        # First handle keyboard input
        original_handle_input(self)
        
        # Then add gyro input if available
        if hasattr(self, 'using_gyro') and self.using_gyro:
            # Get rotation from gyroscope and add it to current velocity
            gyro_velocity = self.gyro.get_rotation(PLAYER_SPEED)
            # If keyboard input is being used (velocity is non-zero), don't override it
            if self.player.velocity_x == 0:
                self.player.velocity_x = gyro_velocity
    
    game_class.__init__ = new_init
    game_class.handle_input = new_handle_input
    
    return game_class