
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AWSMqttConfig(BaseModel):
    endpoint: str = Field(..., description="AWS IoT Core endpoint")
    port: int = Field(default=8883, description="MQTT port")
    topic: str = Field(default="sdk/test/python", description="MQTT topic")
    keepalive: int = Field(default=60, description="MQTT keepalive timeout in seconds")
    client_id: str = Field(default="basicPubSub", description="MQTT client ID")
    qos: int = Field(default=1, ge=0, le=2, description="MQTT Quality of Service level")
    root_ca: str = Field(default="certs/your-device-certificate.pem.crt", description="Root CA certificate path")
    cert_file: str = Field(default="certs/your-AmazonRootCA1.pem", description="Device certificate path")
    private_key: str = Field(default="certs/your-private.pem.key", description="Private key path")


class SensorConfig(BaseModel):
    device_id: str = Field(default="sensor-001", description="Sensor device identifier")
    interval: int = Field(default=5, ge=1, description="Data collection interval in seconds")
    random_seed: int = Field(default=42, description="Random seed for reproducible data generation")

class AWSSqsConfig(BaseModel):
    queue_url: str = Field(..., description="SQS Queue URL")
    region: str = Field(default="us-east-1", description="AWS region")
    message_group_id: str = Field(default="", description="Message group ID for FIFO queues (leave empty for Standard)")

class Config(BaseSettings):
    log_level: str = Field(default="INFO", description="Logging level")
    aws_access_key_id: str = Field(default="", description="AWS Access Key ID")
    aws_secret_access_key: str = Field(default="", description="AWS Secret Access Key")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    
    # Nested configurations
    aws_mqtt: AWSMqttConfig = Field(default_factory=AWSMqttConfig)
    aws_sqs: AWSSqsConfig = Field(default_factory=AWSSqsConfig)
    sensor: SensorConfig = Field(default_factory=SensorConfig)
    

config = Config()
