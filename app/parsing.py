# app/parsing.py
import pdfplumber
import docx2txt
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += " " + page_text
    return clean_text(text)

def parse_docx(path):
    text = docx2txt.process(path) or ""
    return clean_text(text)
