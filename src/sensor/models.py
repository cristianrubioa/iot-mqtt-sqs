from pydantic import BaseModel

class SensorData(BaseModel):
    device_id: str
    timestamp: str
    temperature: float
    humidity: float
    
    def to_json(self) -> str:
        return self.model_dump_json()
