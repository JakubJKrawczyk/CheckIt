from ..models.webservice.comparer_core.IData_core import FileType
from typing import Any
from pandas import DataFrame


class Comparator:

    def __init__(self):

        pass
    
    def compare(self,df1: DataFrame, df2: DataFrame ) -> list[dict] | Exception: 
        
        differences = []
        try:
            
            if df1.shape != df2.shape:
                return Exception(f"DataFrames mają różne wymiary: {df1.shape} vs {df2.shape}")
            if not df1.columns.equals(df2.columns):
                return Exception(f"DataFrames mają różne kolumny: {list(df1.columns)} vs {list(df2.columns)}")


            mask = df1 != df2

            for idx in df1.index:
                for col in df1.columns:
                    if mask.loc[idx, col]:
                        differences.append({
                        "index": idx,
                        "column": col,
                        "value1": df1.loc[idx, col],
                        "value2": df2.loc[idx, col]
                    })
            
            return differences
        except Exception as e:
            return e
       

comparator = Comparator()