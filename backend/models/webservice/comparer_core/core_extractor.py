from abc import ABC, abstractmethod
from typing import Any, List

class IDataExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str, address: Any) -> Any:
        pass