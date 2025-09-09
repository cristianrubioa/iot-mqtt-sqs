from dataclasses import dataclass
from src.sensor.base import BaseSensor
from typing import Any


@dataclass 
class RealSensor(BaseSensor):
    def read_data(self) -> Any:
        # TODO: Read actual sensor data from hardware (GPIO, I2C, SPI, etc.)
        ...
