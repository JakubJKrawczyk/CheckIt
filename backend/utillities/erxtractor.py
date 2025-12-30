from ..models.webservice.comparer_core.extraction_strategies.excel_extractor import ExcelExtractor

class Extractor:
    def __init__(self):
        self.excel_extractor = ExcelExtractor()

extractor = Extractor()