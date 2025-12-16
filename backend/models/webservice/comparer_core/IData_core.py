from enum import Enum
from typing import List, Optional, Union, Any
from pydantic import BaseModel
import pandas as pd


class FileType(Enum):
    PDF=0,
    EXCEL=1
    
class IDataCore(BaseModel):
    key_column_name: str
    file_type: FileType
    df: pd.DataFrame

    @property
    def rows(self):
        return self.df.shape[0]
    
    @property
    def col_names(self):
        return self.df.columns

    def get_value(self, column: str, row: int):
        return self.df.at[row, column]

    class Config:
        arbitrary_types_allowed = True