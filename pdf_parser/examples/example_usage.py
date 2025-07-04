import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from pdf_parser.parser import PDFParser

if __name__ == "__main__":
    # Always resolve the PDF path relative to the project root
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.pdf'))
    parser = PDFParser(pdf_path)
    text = parser.extract_text()
    images = parser.extract_images()
    sections = parser.parse_sections()

    print("="*40)
    print("EXTRACTED TEXT")
    print("="*40)
    print(text)
    print("\n" + "="*40)
    print("EXTRACTED IMAGES")
    print("="*40)
    for img in images:
        print(f"- {img}")
    if not images:
        print("No images extracted.")
    print("\n" + "="*40)
    print("PARSED SECTIONS")
    print("="*40)
    for heading, content in sections.items():
        print(f"\n{heading}\n{'-'*len(heading)}\n{content}\n")