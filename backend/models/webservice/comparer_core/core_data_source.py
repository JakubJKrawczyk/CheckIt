from enum import Enum
from typing import List, Optional, Union, Any
from pydantic import BaseModel

class SourceType(Enum):
    EXCEL_COLUMN = "excel_column"
    PDF_REGION = "pdf_region"

# Adres danych - "gdzie to jest?"
class DataAddress(BaseModel):
    source_type: SourceType
    # Dla Excela:
    sheet_name: Optional[str] = None
    column_letter: Optional[str] = None
    row_index: Optional[int] = None
    # Dla PDF:
    page_number: Optional[int] = None
    bbox: Optional[List[float]] = None # [x, y, width, height]

# Reguła ekstrakcji - jedna para do porównania
class ComparisonRule(BaseModel):
    field_name: str  # np. "Numer Faktury"
    source_a: DataAddress
    source_b: DataAddress
    tolerance: float = 0.0 # np. dla liczb, czy akceptujemy różnicę 0.01