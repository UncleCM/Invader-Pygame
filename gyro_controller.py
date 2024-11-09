import time
from mpu6050 import mpu6050

class GyroController:
    def __init__(self, sensitivity: float = 15.0):
        """
        Initialize the gyroscope controller.
        
        Args:
            sensitivity: Multiplier for converting gyro readings to player movement
        """
        try:
            # Initialize the MPU6050 with default I2C address (0x68)
            self.sensor = mpu6050(0x68)
            
            # Set sensitivity multiplier
            self.sensitivity = sensitivity
            
            # Calibrate the sensor
            print("Calibrating gyroscope... Keep the device still.")
            self.calibration_offset = self._calibrate()
            print("Calibration complete!")
            
        except Exception as e:
            print(f"Failed to initialize MPU6050: {e}")
            raise

    def _calibrate(self, samples: int = 100) -> float:
        """
        Calibrate the gyroscope by taking multiple readings at rest.
        Returns the average offset to be subtracted from future readings.
        
        Args:
            samples: Number of samples to take for calibration
            
        Returns:
            float: The average z-axis offset
        """
        total = 0
        for _ in range(samples):
            try:
                gyro_data = self.sensor.get_gyro_data()
                total += gyro_data['x']
                time.sleep(0.01)
            except Exception as e:
                print(f"Error during calibration: {e}")
                continue
        return total / samples

    def get_rotation(self, max_speed: float) -> float:
        """
        Get the current rotation rate from the gyroscope.
        Movement is inverted so tilting right moves player left and vice versa.
        
        Args:
            max_speed: Maximum allowed speed for player movement
            
        Returns:
            float: A value suitable for player movement speed, clamped between -max_speed and max_speed
        """
        try:
            # Get gyro data
            gyro_data = self.sensor.get_gyro_data()
            z_rotation = gyro_data['x']
            
            # Apply calibration offset
            adjusted_rotation = z_rotation - self.calibration_offset
            
            # Apply sensitivity and convert to movement value
            # Negative sign inverts the movement direction
            movement = -1 * adjusted_rotation * self.sensitivity
            
            # Clamp the value to max_speed
            return max(min(movement, max_speed), -max_speed)
            
        except Exception as e:
            print(f"Error reading gyroscope: {e}")
            raise

    def cleanup(self):
        """
        Clean up resources. Currently a placeholder as mpu6050 doesn't require cleanup.
        """
        pass