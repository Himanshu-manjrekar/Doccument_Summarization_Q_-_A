import streamlit as st
import fitz
from docx import Document
from transformers import pipeline
from src.utils import *
from src.summarizer import summarizer

# Load Hugging Face Summarization Model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def extract_text(file):
#     """Extract text from uploaded document"""
#     if file.type == "application/pdf":
#         reader = PdfReader(file)
#         return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
#     elif file.type == "text/plain":  # TXT files
#         return file.read().decode("utf-8")
#     elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # DOCX
#         doc = docx.Document(file)
#         return "\n".join([para.text for para in doc.paragraphs])
#     else:
#         return None

# def summarize_text(text):
#     """Summarize the extracted text"""
#     return summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

def chat_with_text_ui():
    """Display chat UI"""
    st.session_state.chat_mode = True
    # st.experimental_user()

# Streamlit UI
st.set_page_config(page_title="Document Chat & Summarizer", layout="wide")

with st.container():
    st.title("📄 Document Summarizer & Chat")
    # st.write("")
    uploaded_file = st.file_uploader("Upload a document and choose an action.", type=["pdf", "txt", "docx"])
    
    col1, col2 = st.columns(2)
    with col1:
        summarize_btn = st.button("📄 Summarize Document")
    with col2:
        chat_btn = st.button("💬 Chat with Document", on_click=chat_with_text_ui)

# Handling Summarization
if summarize_btn and uploaded_file:
    chunks = Operation_handler(uploaded_file)
    if chunks_of_text:
        summarizer = summarizer()
        summary = summarizer.summarize_the_data(chunks)
        st.subheader("🔍 Summary:")
        st.write(summary)
        # st.write(uploaded_file.name)
        # st.write("Content of file: ",chunks)
    else:
        st.error("Failed to extract text. Please upload a valid document.")

# Handling Chat UI
if "chat_mode" in st.session_state and st.session_state.chat_mode:
    st.subheader("💬 Chat with Your Document")
    user_input = st.text_input("Ask a question about the document:")
    if user_input:
        st.write(f"**AI:** {user_input} (This is where the LLM response will go)")

