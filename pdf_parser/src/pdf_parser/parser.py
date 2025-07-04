import PyPDF2
from .utils import clean_text
from PIL import Image
import pytesseract
import io
import os
import re

class PDFParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self, clean=True, ocr=False):
        text = ""
        with open(self.file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if not page_text and ocr:
                    # Try OCR if no text extracted
                    try:
                        images = self._page_images(page)
                        for img in images:
                            ocr_text = pytesseract.image_to_string(img)
                            text += ocr_text + "\n"
                    except Exception as e:
                        print(f"OCR failed on page {page_num+1}: {e}")
                elif page_text:
                    text += page_text + "\n"
        if clean:
            text = clean_text(text)
        return text

    def _page_images(self, page):
        # Extract images from a PDF page for OCR
        images = []
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    img = xObject[obj]
                    data = img.get_data()
                    try:
                        image = Image.open(io.BytesIO(data))
                        images.append(image)
                    except Exception:
                        continue
        return images

    def parse_sections(self):
        """
        Parse the extracted text into sections based on numbered headings (e.g., '1. Introduction').
        Returns a dict: {section_title: section_content}
        """
        text = self.extract_text()
        # Regex to find section headings like '1. Introduction', '2. TCP', etc.
        pattern = re.compile(r'(?P<heading>\d+\.\s+[A-Z][^\n]*)')
        matches = list(pattern.finditer(text))
        sections = {}
        for i, match in enumerate(matches):
            start = match.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            heading = match.group('heading').strip()
            content = text[start:end].strip()
            sections[heading] = content
        return sections

    def extract_images(self, output_folder="extracted_images"):
        os.makedirs(output_folder, exist_ok=True)
        images = []
        with open(self.file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                if '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()
                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            img = xObject[obj]
                            data = img.get_data()
                            # Handle JPEG images
                            if img.get('/Filter') == '/DCTDecode':
                                img_ext = 'jpg'
                                img_name = f"{output_folder}/page{page_num+1}_{obj[1:]}.{img_ext}"
                                with open(img_name, "wb") as img_file:
                                    img_file.write(data)
                                images.append(img_name)
                            # Handle PNG-like images
                            elif img.get('/Filter') == '/FlateDecode':
                                try:
                                    img_ext = 'png'
                                    img_name = f"{output_folder}/page{page_num+1}_{obj[1:]}.{img_ext}"
                                    image = Image.open(io.BytesIO(data))
                                    image.save(img_name)
                                    images.append(img_name)
                                except Exception as e:
                                    print(f"Skipping image {obj}: {e}")
                            else:
                                print(f"Skipping image {obj}: unsupported filter {img.get('/Filter')}")
        return images