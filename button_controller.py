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
        GPIO.setwarnings(False)  # Disable warnings
        
        # Configure with pull-up resistor
        # When button is pressed, it will connect to ground (GPIO.LOW)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Debouncing variables
        self.last_press_time = 0
        self.debounce_time = 0.05  # Reduce debounce time to 50ms for better responsiveness
        
    def is_pressed(self) -> bool:
        """
        Check if button is pressed, with debouncing.
        
        Returns:
            bool: True if button is pressed, False otherwise
        """
        # Note: With pull-up resistor, GPIO.LOW means button is pressed
        button_state = GPIO.input(self.pin) == GPIO.LOW
        
        if button_state:
            current_time = time.time()
            if current_time - self.last_press_time > self.debounce_time:
                self.last_press_time = current_time
                return True
        return False
    
    def cleanup(self):
        """Clean up GPIO on exit"""
        GPIO.cleanup(self.pin)  # Only clean up our pin