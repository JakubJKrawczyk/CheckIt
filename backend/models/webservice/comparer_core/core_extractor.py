from abc import ABC, abstractmethod
from typing import Any, List
from backend.models.webservice.comparer_core.IData_core import DataAddress

class IDataExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str, address: DataAddress) -> List[Any]:
        pass