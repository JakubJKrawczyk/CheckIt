from ..models.webservice.comparer_core.IData_core import FileType
from typing import Any
from pandas import DataFrame


class Comparator:

    def __init__(self):

        pass
    
    def compare(self,df1: DataFrame, df2: DataFrame, column_pairs: list[dict]) -> list[dict] | Exception: 
        
        differences = []
        try:
            
            if df1.shape != df2.shape:
                return Exception(f"DataFrames mają różne wymiary: {df1.shape} vs {df2.shape}")
            if not df1.columns.equals(df2.columns):
                return Exception(f"DataFrames mają różne kolumny: {list(df1.columns)} vs {list(df2.columns)}")
            if pair is None | pair["column1"] is None | pair["column2"] is None:
                 return Exception(f"Compare wymaga podania przynajmniej jedną parę kolumn, które chce się porównać!")

            

            for idx in df1.index:
                for pair in column_pairs:
                    if df1[idx, pair["column1"]] != df2[idx, pair["column2"]]:
                        differences.append({
                        "index": idx,
                        "columns": f"{pair["column1"]}:{pair["column2"]}",
                        "value1": df1.loc[idx, pair["column1"]],
                        "value2": df2.loc[idx, pair["column2"]]
                         })
            
            return differences
        except Exception as e:
            return e
       

comparator = Comparator()