import os
import csv
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTImage
from PIL import Image
import pytesseract
import io

# PDF_PATH = os.path.join(os.path.dirname(__file__), '../data/sample.pdf')
PDF_PATH = os.path.join(os.path.dirname(__file__), "Backlog Seating Arrangement 17.06 Afternoon.pdf")
CSV_OUTPUT = os.path.join(os.path.dirname(__file__), 'sample_table_output.csv')

def extract_table_like_text(pdf_path):
    """
    Extracts table-like text from a PDF using text positions from both
    text elements and OCR'd images.
    Returns a list of rows (each row is a list of cell strings).
    """
    all_text_elements = []
    page_count = 0
    for page_layout in extract_pages(pdf_path):
        page_count += 1
        print(f"--- Processing Page {page_layout.pageid} ---")
        page_height = page_layout.height
        
        text_count = 0
        image_count = 0
        # Collect all text elements with their coordinates
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_count += 1
                for text_line in element:
                    if hasattr(text_line, 'get_text'):
                        text = text_line.get_text().strip()
                        if text:
                            # Use the y0 coordinate (bottom of the text box)
                            y0 = round(text_line.y0, 1)
                            all_text_elements.append((y0, text_line.x0, text))
            
            # OCR for images
            if isinstance(element, LTImage):
                image_count += 1
                try:
                    img_stream = element.stream.get_data()
                    img = Image.open(io.BytesIO(img_stream))
                    
                    # Get OCR data with bounding boxes
                    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                    
                    img_x0, img_y0, img_x1, img_y1 = element.bbox
                    
                    for i, text in enumerate(ocr_data['text']):
                        if text.strip():
                            # OCR coordinates are relative to the image
                            ocr_x = ocr_data['left'][i]
                            ocr_y = ocr_data['top'][i]
                            ocr_h = ocr_data['height'][i]
                            
                            # Translate image coords to page coords
                            page_x = img_x0 + ocr_x
                            # PDF y-origin is bottom-left, image y-origin is top-left
                            page_y = img_y1 - ocr_y - ocr_h 
                            
                            all_text_elements.append((page_y, page_x, text.strip()))
                except Exception as e:
                    print(f"Skipping image on page {page_layout.pageid}, could not process: {e}")

        print(f"Found {text_count} text containers and {image_count} images on page {page_layout.pageid}.")

    print(f"\nFinished processing {page_count} pages.")
    print(f"Total text elements collected: {len(all_text_elements)}")
    if all_text_elements:
        print(f"First 5 elements found: {all_text_elements[:5]}")

    # Group by y-coordinate (row)
    all_text_elements.sort(key=lambda x: (-x[0], x[1])) # Sort top-to-bottom, then left-to-right
    
    rows = []
    if not all_text_elements:
        return rows

    current_row = [all_text_elements[0]]
    last_y = all_text_elements[0][0]

    for i in range(1, len(all_text_elements)):
        y0, x0, text = all_text_elements[i]
        # Use a tolerance to group lines that are on the same visual row
        if abs(y0 - last_y) < 5: # 5 units tolerance for same line
            current_row.append(all_text_elements[i])
        else:
            # New row detected, save the old one
            current_row.sort(key=lambda x: x[1]) # Sort cells by x-coordinate
            print(f"DEBUG: Row found with y ~ {last_y:.2f}: {[cell[2] for cell in current_row]}")
            if len(current_row) > 1: # Only consider rows with more than one "cell"
                rows.append([cell[2] for cell in current_row])
            current_row = [all_text_elements[i]]
            last_y = y0
    
    # Add the last processed row
    if current_row:
        current_row.sort(key=lambda x: x[1])
        print(f"DEBUG: Last row found with y ~ {last_y:.2f}: {[cell[2] for cell in current_row]}")
        if len(current_row) > 1:
            rows.append([cell[2] for cell in current_row])

    print(f"Total multi-column rows formed: {len(rows)}")
    return rows

def save_rows_to_csv(rows, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

if __name__ == '__main__':
    print(f"Processing {PDF_PATH}...")
    rows = extract_table_like_text(PDF_PATH)
    if rows:
        save_rows_to_csv(rows, CSV_OUTPUT)
        print(f"Extracted table-like data and saved to {CSV_OUTPUT}")
    else:
        print("No table-like data found.") 