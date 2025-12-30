from ..core_extractor import IDataExtractor
from typing import Any

class ExcelExtractor(IDataExtractor):
    def extract(self, file_path: str, key_col_name: str) -> list:
        import pandas as pd
        df = pd.read_excel(file_path, index_col=key_col_name)
        return df