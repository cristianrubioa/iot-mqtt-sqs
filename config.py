
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class AWSMqttConfig(BaseModel):
    endpoint: str = Field(..., description="AWS IoT Core endpoint")
    port: int = Field(default=8883, description="MQTT port")
    topic: str = Field(default="sensor/data", description="MQTT topic")
    keepalive: int = Field(default=60, description="MQTT keepalive timeout in seconds")
    root_ca: str = Field(default="certs/AmazonRootCA1.pem", description="Root CA certificate path")
    cert_file: str = Field(default="certs/device-certificate.pem.crt", description="Device certificate path")
    private_key: str = Field(default="certs/private.pem.key", description="Private key path")


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
    
    # Nested configurations
    aws_mqtt: AWSMqttConfig = Field(default_factory=AWSMqttConfig)
    sensor: SensorConfig = Field(default_factory=SensorConfig)
    
    # General settings
    log_level: str = Field(default="INFO", description="Logging level")

# Singleton instance
config = Config()
