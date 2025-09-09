
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class SensorConfig(BaseModel):
    device_id: str = Field(default="sensor-001", description="Sensor device identifier")
    interval: int = Field(default=5, ge=1, description="Data collection interval in seconds")
    random_seed: int = Field(default=42, description="Random seed for reproducible data generation")

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    
    sensor: SensorConfig = Field(default_factory=SensorConfig)
    
    # General settings
    log_level: str = Field(default="INFO", description="Logging level")

# Singleton instance
config = Config()
