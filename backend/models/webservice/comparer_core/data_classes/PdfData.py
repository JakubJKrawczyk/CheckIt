from ..IData_core import IDataCore, FileType
import pandas as pd
from ....internal.pdf_region import pdf_region

class PDFRegionColumn():

    def __init__(self, column: str, region: pdf_region, page: int):
        self.column = column
        self.region = region
        self.page = page

class PdfData(IDataCore):

    def __init__(self, key_col_name: str, data: pd.DataFrame, regions: list[PDFRegionColumn]):
        super.__init__(key_col_name=key_col_name,file_type=FileType.PDF , df=data)
        self.regions = regions

    