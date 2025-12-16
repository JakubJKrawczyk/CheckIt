from abc import ABC, abstractmethod
from typing import Any, List
from backend.models.webservice.comparer_core.core_data_source import DataAddress

class IDataExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str, address: DataAddress) -> List[Any]:
        pass