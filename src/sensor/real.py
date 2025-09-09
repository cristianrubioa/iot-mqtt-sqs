from dataclasses import dataclass
from src.sensor.base import BaseSensor
from src.sensor.models import SensorData


@dataclass 
class RealSensor(BaseSensor):
    def generate_data(self) -> SensorData:
        # TODO: Read actual sensor data from hardware (GPIO, I2C, SPI, etc.)
        ...
