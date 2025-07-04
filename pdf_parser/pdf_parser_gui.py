import sys
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from pdf_parser.parser import PDFParser

def select_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, file_path)
        status_var.set(f"Selected: {os.path.basename(file_path)}")

def parse_pdf():
    pdf_path = entry_pdf.get()
    if not os.path.isfile(pdf_path):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return
    ocr_enabled = ocr_var.get()
    parser = PDFParser(pdf_path)
    text = parser.extract_text(ocr=ocr_enabled)
    sections = parser.parse_sections()
    images = parser.extract_images()
    # Show text
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, "EXTRACTED TEXT\n" + "="*40 + "\n")
    text_box.insert(tk.END, text + "\n\n")
    text_box.insert(tk.END, "PARSED SECTIONS\n" + "="*40 + "\n")
    for heading, content in sections.items():
        text_box.insert(tk.END, f"\n{heading}\n{'-'*len(heading)}\n{content}\n")
    text_box.insert(tk.END, "\nEXTRACTED IMAGES\n" + "="*40 + "\n")
    for img in images:
        text_box.insert(tk.END, f"- {img}\n")
    if not images:
        text_box.insert(tk.END, "No images extracted.\n")
    status_var.set(f"Parsed: {os.path.basename(pdf_path)} | Text: {len(text)} chars | Images: {len(images)} | OCR: {'On' if ocr_enabled else 'Off'}")

def clear_all():
    entry_pdf.delete(0, tk.END)
    text_box.delete(1.0, tk.END)
    status_var.set("Ready.")
    ocr_var.set(False)

root = tk.Tk()
root.title("PDF Parser App")
root.geometry("1100x800")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill='x')

label_pdf = tk.Label(frame, text="PDF File:")
label_pdf.grid(row=0, column=0, sticky="e")
entry_pdf = tk.Entry(frame, width=60)
entry_pdf.grid(row=0, column=1, padx=5)
btn_browse = tk.Button(frame, text="Browse...", command=select_pdf)
btn_browse.grid(row=0, column=2, padx=5)
btn_parse = tk.Button(frame, text="Parse PDF", command=parse_pdf)
btn_parse.grid(row=0, column=3, padx=5)
btn_clear = tk.Button(frame, text="Clear", command=clear_all)
btn_clear.grid(row=0, column=4, padx=5)

ocr_var = tk.BooleanVar()
ocr_checkbox = tk.Checkbutton(frame, text="Enable OCR (for scanned PDFs)", variable=ocr_var)
ocr_checkbox.grid(row=0, column=5, padx=10)

# Status bar
status_var = tk.StringVar()
status_var.set("Ready.")
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor='w')
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Tab 1: Full Text & Sections
frame_text = tk.Frame(notebook)
notebook.add(frame_text, text="Text & Sections")
text_box = scrolledtext.ScrolledText(frame_text, width=120, height=40)
text_box.pack(fill='both', expand=True)

# Tab 2: Images (list only, for now)
frame_images = tk.Frame(notebook)
notebook.add(frame_images, text="Images")
images_box = scrolledtext.ScrolledText(frame_images, width=120, height=40)
images_box.pack(fill='both', expand=True)

# Enhance parse_pdf to also show images in the Images tab
old_parse_pdf = parse_pdf
def parse_pdf():
    old_parse_pdf()
    pdf_path = entry_pdf.get()
    if not os.path.isfile(pdf_path):
        return
    parser = PDFParser(pdf_path)
    images = parser.extract_images()
    images_box.delete(1.0, tk.END)
    if images:
        images_box.insert(tk.END, "Extracted Images:\n" + "-"*40 + "\n")
        for img in images:
            images_box.insert(tk.END, f"- {img}\n")
    else:
        images_box.insert(tk.END, "No images extracted.\n")

root.mainloop()