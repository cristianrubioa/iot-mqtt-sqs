from abc import ABC, abstractmethod
from typing import Any

class BaseSensor(ABC):
    @abstractmethod
    def read_data(self) -> Any:
        ...