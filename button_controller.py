import RPi.GPIO as GPIO
import time

class ButtonController:
    def __init__(self, pin: int = 17):
        """
        Initialize the button controller.
        
        Args:
            pin: GPIO pin number for the button (BCM numbering)
        """
        self.pin = pin
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Debouncing variables
        self.last_press_time = 0
        self.debounce_time = 0.1  # 100ms debounce
        
    def is_pressed(self) -> bool:
        """
        Check if button is pressed, with debouncing.
        
        Returns:
            bool: True if button is pressed, False otherwise
        """
        current_time = time.time()
        
        # Check if button is pressed (GPIO.LOW due to pull-up)
        if GPIO.input(self.pin) == GPIO.LOW:
            # Check if enough time has passed since last press
            if current_time - self.last_press_time > self.debounce_time:
                self.last_press_time = current_time
                return True
        return False
    
    def cleanup(self):
        """Clean up GPIO on exit"""
        GPIO.cleanup()