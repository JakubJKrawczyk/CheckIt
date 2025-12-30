from ..models.webservice.comparer_core.IData_core import FileType
from typing import Any

class Comparator:

    def __init__(self):

        pass
    
    def compare(self,file_data1: Any, file_type1: FileType, file_data2: Any, file_type2: FileType ) -> list[int] | Exception:
        
        if file_type1 == FileType.EXCEL and file_type2 == FileType.EXCEL:
            
            
            return []
        else:
             return Exception("Podane zestawienie plików nie jest obsługiwane!")

comparator = Comparator()