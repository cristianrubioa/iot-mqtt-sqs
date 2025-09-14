from abc import ABC, abstractmethod
from typing import Any, List, Dict

class BaseSQSClient(ABC):
    @abstractmethod
    def send_message(self, data: Any) -> bool:
        ...
    
    @abstractmethod
    def receive_messages(self, max_messages: int) -> List[Dict[str, Any]]:
        ...
    
    @abstractmethod
    def delete_message(self, receipt_handle: str) -> bool:
        ...
    
    @abstractmethod
    def is_connected(self) -> bool:
        ...
