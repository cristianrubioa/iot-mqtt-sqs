from abc import ABC, abstractmethod
from typing import Any

class BaseSQSClient(ABC):
    @abstractmethod
    def send_message(self, data: Any) -> bool:
        ...
    
    @abstractmethod
    def is_connected(self) -> bool:
        ...
