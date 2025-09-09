import ssl
import logging
from dataclasses import dataclass
from typing import Any
from paho.mqtt import client as mqtt_client
from src.mqtt_publisher.base import BasePublisher
from config import config

logger = logging.getLogger(__name__)

@dataclass
class AWSMQTTPublisher(BasePublisher):
    def __post_init__(self) -> None:
        super().__post_init__()
        self._setup_ssl()
        
    def _setup_ssl(self) -> None:
        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations(config.aws_mqtt.root_ca)
            context.load_cert_chain(config.aws_mqtt.cert_file, config.aws_mqtt.private_key)
            self.client.tls_set_context(context)
        except Exception as e:
            logger.error(f"SSL setup failed: {e}")
            raise
    def connect(self) -> None:
        try:
            self.client.connect(config.aws_mqtt.endpoint, config.aws_mqtt.port, config.aws_mqtt.keepalive)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
        
    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
        
    def publish(self, data: Any) -> bool:
        try:
            if hasattr(data, "to_json"):
                payload = data.to_json()
            else:
                payload = str(data)
            
            result = self.client.publish(config.aws_mqtt.topic, payload)
            if result.rc != mqtt_client.MQTT_ERR_SUCCESS:
                logger.error(f"Failed to publish: {result.rc}")
                return False
            return True
        except Exception as e:
            logger.error(f"Publish error: {e}")
            return False

    def is_connected(self) -> bool:
        return self.client.is_connected()
