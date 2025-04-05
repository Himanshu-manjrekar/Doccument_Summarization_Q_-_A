import os
import re

from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Extract PDF's
def extract_pdf(uploaded_file):
    # doc = fitz.open(file_path)
    doc = PdfReader(uploaded_file)
    text = ""
    for page in doc.pages:
        text += page.extract_text()
    return text

# Extract Docx Files
def extract_doc(uploaded_file):
    doc = Document(uploaded_file)
    text = "\n".join([data.text for data in doc.paragraphs])
    return text

# Extract txt Files
def extract_txt(uploaded_file):
    data = open(uploaded_file,"r").read()
    return data

# Cleaning the extracted text
def clean_text(text):
     # Replace multiple newlines with a single newline (preserves paragraphs)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text  = re.sub(r'[^\x00-\x7F]+', " ", text) ## hyper links are highlighted as "\xa0" so we will remove this
    return text

# making chunks of 1000 words with overlap of 50 words
def chunks_of_text(extracted_text):
    cleaned_text = clean_text(extracted_text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 50)
    chunks = text_splitter.split_text(cleaned_text)
    print("length of chunks:- ", len(chunks))
    return chunks


def Operation_handler(file):
    # First we will check the file type and execute the appropriate I/O operation
    if file.type == "application/pdf":
        text = extract_pdf(file)   # This will return the text
        chunks = chunks_of_text(text)
        return chunks
    elif file.type == "text/plain":  # TXT files
        text = extract_txt(file)
        chunks = chunks_of_text(text)
        return chunks
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # DOCX files
        text = extract_doc(file)
        chunks = chunks_of_text(text)
        return chunks
    else:
        return None # we need to handle this in Future