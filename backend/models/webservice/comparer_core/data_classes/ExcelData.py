from ..IData_core import IDataCore, FileType
import pandas as pd

class ExcelData(IDataCore):

    def __init__(self, key_col_name: str, data: pd.DataFrame):
        super.__init__(key_col_name,FileType.EXCEL , data)

