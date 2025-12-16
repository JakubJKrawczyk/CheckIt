from ..core_extractor import IDataExtractor
from ..IData_core import DataAddress

class ExcelExtractor(IDataExtractor):
    def extract(self, file_path: str, address: DataAddress) -> list:
        import pandas as pd
        df = pd.read_excel(file_path, sheet_name=address.sheet_name)
        return df[address.column_letter][address.row_index].tolist()