import RPi.GPIO as GPIO
import smbus
from typing import Tuple
import config

class HardwareController:
    def __init__(self):
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Initialize I2C
        self.bus = smbus.SMBus(1)
        self.last_x_reading = 0
        
        # Wake up MPU6050
        try:
            self.bus.write_byte_data(config.MPU_ADDR, config.POWER_MGMT_1, 0)
        except Exception as e:
            print(f"Error initializing MPU6050: {e}")
            
    def read_gyro(self) -> float:
        try:
            high = self.bus.read_byte_data(config.MPU_ADDR, config.ACCEL_XOUT)
            low = self.bus.read_byte_data(config.MPU_ADDR, config.ACCEL_XOUT + 1)
            value = (high << 8) | low
            
            if value >= 0x8000:
                value = -((65535 - value) + 1)
            
            return value / 16384.0
        except Exception as e:
            print(f"Error reading gyroscope: {e}")
            return 0
            
    def get_movement(self) -> float:
        x_accel = self.read_gyro()
        self.last_x_reading = self.last_x_reading * 0.7 + x_accel * 0.3
        return -self.last_x_reading * config.GYRO_SENSITIVITY * config.PLAYER_SPEED
        
    def is_shooting(self) -> bool:
        return not GPIO.input(config.BUTTON_PIN)
        
    def cleanup(self):
        GPIO.cleanup()