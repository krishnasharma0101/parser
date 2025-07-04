from .parser import PDFParser

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.pdf_parser.main <pdf_file>")
        return
    file_path = sys.argv[1]
    parser = PDFParser(file_path)
    text = parser.extract_text()
    print(text)

if __name__ == "__main__":
    main()