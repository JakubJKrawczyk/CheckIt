from ..core_extractor import IDataExtractor
from ..core_data_source import DataAddress

class PDFRegionExt(IDataExtractor):
    def extract(self, file_path: str, address: DataAddress) -> list:
        from paddleocr import PaddleOCR
        import pymupdf  # PyMuPDF
        doc = pymupdf.open(file_path)
        if address.page_number is None or address.bbox is None:
            raise ValueError("For PDF_REGION, page_number and bbox must be provided")
        
        page = doc.load_page(address.page_number - 1)
        pix = page.get_pixmap(clip=address.bbox)
        image = pix.tobytes("png")

        ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)
        result = ocr.predict(image)
        extracted_texts = result
        print(extracted_texts)

        return extracted_texts