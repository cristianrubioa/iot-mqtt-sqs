import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Type
from paho.mqtt import client as mqtt_client

logger = logging.getLogger(__name__)

class BasePublisher(ABC):
    def __post_init__(self) -> None:
        self.client = mqtt_client.Client()
        self._setup_callbacks()
    
    def _setup_callbacks(self) -> None:
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
    
    def _on_connect(self, client: mqtt_client.Client, userdata: Any, flags: dict, rc: int) -> None:
        del client, userdata, flags
        if rc == 0:
            logger.info("Connected to MQTT broker")
        else:
            logger.error(f"Connection failed with code {rc}")
            
    def _on_disconnect(self, client: mqtt_client.Client, userdata: Any, rc: int) -> None:
        del client, userdata
        logger.warning(f"Disconnected from MQTT broker (code: {rc})")
        
    def _on_publish(self, client: mqtt_client.Client, userdata: Any, mid: int) -> None:
        del client, userdata
        logger.debug(f"Message {mid} published successfully")
    
    @abstractmethod
    def connect(self) -> None:
        ...
    
    @abstractmethod
    def disconnect(self) -> None:
        ...
    
    @abstractmethod
    def publish(self, data: Any) -> bool:
        ...
    
    @abstractmethod
    def is_connected(self) -> bool:
        ...
    
    def __enter__(self) -> "BasePublisher":
        self.connect()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        del exc_type, exc_val, exc_tb
        self.disconnect()
