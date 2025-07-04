import os
import re

def is_pdf(file_path):
    return os.path.isfile(file_path) and file_path.lower().endswith('.pdf')

def clean_text(text):
    # Replace multiple newlines with two newlines (paragraphs)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove leading/trailing whitespace on each line
    text = '\n'.join(line.strip() for line in text.splitlines())
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()