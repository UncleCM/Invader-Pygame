from typing import Type
from gyro_controller import GyroController

def add_gyro_controls(game_class: Type) -> Type:
    """
    Decorator to add gyroscope controls to the game class.
    
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
        if hasattr(self, 'using_gyro') and self.using_gyro:
            # Get rotation from gyroscope, using the class's PLAYER_SPEED constant
            self.player.velocity_x = self.gyro.get_rotation(self.PLAYER_SPEED)
        else:
            # Fall back to original keyboard controls
            original_handle_input(self)
    
    game_class.__init__ = new_init
    game_class.handle_input = new_handle_input
    
    return game_class
