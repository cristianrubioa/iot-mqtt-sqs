
import random
from datetime import datetime, timezone
from dataclasses import dataclass
from src.sensor.base import BaseSensor
from src.sensor.models import SensorData
from config import config

random.seed(config.sensor.random_seed)

@dataclass
class SimulatedSensor(BaseSensor):
    device_id: str
    base_temperature: float = 22.0
    temperature_variation: float = 4.0  
    base_humidity: float = 45.0
    humidity_variation: float = 15.0
        
    def generate_data(self) -> SensorData:
        """Generate realistic sensor data with natural variation
        
        Temperature varies around base_temperature ± temperature_variation.
        Humidity varies around base_humidity ± humidity_variation.
        Timestamp is in ISO format with UTC timezone.
        
        Returns:
            SensorData: Object containing device_id, timestamp, temperature and humidity
        """
        temperature = self.base_temperature + random.uniform(-self.temperature_variation, self.temperature_variation)
        temperature = round(temperature, 2)
        
        humidity = self.base_humidity + random.uniform(-self.humidity_variation, self.humidity_variation)
        humidity = max(0.0, min(100.0, round(humidity, 2)))
        
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return SensorData(
            device_id=self.device_id,
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity
        )

