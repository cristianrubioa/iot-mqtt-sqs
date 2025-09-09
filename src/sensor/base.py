from abc import ABC, abstractmethod
from src.sensor.models import SensorData

class BaseSensor(ABC):
    @abstractmethod
    def generate_data(self) -> SensorData:
        ...