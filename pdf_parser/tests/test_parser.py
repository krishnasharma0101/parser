from src.pdf_parser.parser import PDFParser

def test_extract_text():
    parser = PDFParser("data/sample.pdf")
    text = parser.extract_text()
    assert isinstance(text, str)