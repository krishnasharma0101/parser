# PDF Parser

A Python-based PDF parser for extracting text and images from PDF files. This project provides both a command-line interface and a simple GUI for parsing PDFs, extracting images, and processing text using OCR.

## Features
- Extract text from PDF files
- Extract images from PDF files
- OCR support for scanned PDFs using Tesseract
- Command-line and GUI interfaces

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line

Run the CLI script to extract text or images:
```bash
python pdf_parser/scripts/cli.py --help
```

### GUI

Run the GUI application:
```bash
python pdf_parser/pdf_parser_gui.py
```

### Example

See `pdf_parser/examples/example_usage.py` for sample usage.

## Notes
- For OCR functionality, [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) must be installed and available in your system PATH.
- Extracted images and data are saved in the `extracted_images/` and `pdf_parser/extracted_images/` folders.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
See [LICENSE](pdf_parser/LICENSE) for details. 