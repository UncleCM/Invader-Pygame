import smbus
import time
from typing import Tuple

class GyroController:
    # MPU6050 Registers and their Address
    POWER_MGMT_1 = 0x6B
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    INT_ENABLE = 0x38
    GYRO_XOUT = 0x43
    GYRO_YOUT = 0x45
    GYRO_ZOUT = 0x47
    
    def __init__(self, sensitivity: float = 2.0):
        """
        Initialize the gyroscope controller.
        
        Args:
            sensitivity: Multiplier for converting gyro readings to player movement
        """
        # Device address on I2C bus
        self.Device_Address = 0x68
        
        # Initialize I2C bus
        self.bus = smbus.SMBus(1)
        
        # Wake up MPU6050
        self.bus.write_byte_data(self.Device_Address, self.POWER_MGMT_1, 0)
        
        # Configure gyroscope settings
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)
        
        self.sensitivity = sensitivity
        self.calibration_offset = self._calibrate()

    def _read_raw_data(self, addr: int) -> int:
        """Read raw 16-bit value from the gyroscope."""
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr + 1)
        
        value = ((high << 8) | low)
        if value > 32768:
            value = value - 65536
        return value

    def _calibrate(self, samples: int = 100) -> float:
        """
        Calibrate the gyroscope by taking multiple readings at rest.
        Returns the average offset to be subtracted from future readings.
        """
        print("Calibrating gyroscope... Keep the device still.")
        total = 0
        for _ in range(samples):
            total += self._read_raw_data(self.GYRO_ZOUT)
            time.sleep(0.01)
        return total / samples

    def get_rotation(self, max_speed: float) -> float:
        """
        Get the current rotation rate from the gyroscope.
        
        Args:
            max_speed: Maximum allowed speed for player movement
            
        Returns:
            A value suitable for player movement speed.
        """
        z_rotation = self._read_raw_data(self.GYRO_ZOUT)
        adjusted_rotation = (z_rotation - self.calibration_offset) / 131.0  # Convert to degrees/s
        # Apply sensitivity and clamp to reasonable values
        movement = adjusted_rotation * self.sensitivity
        return max(min(movement, max_speed), -max_speed)
