import os
import streamlit as st

from config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    UPLOAD_FOLDER,
    SUPPORTED_FILE_TYPES
)

from utils.parser import (
    save_uploaded_file,
    extract_text
)

# Page Configuration

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# Initialize Session State

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "document_metadata" not in st.session_state:
    st.session_state.document_metadata = {}

# Sidebar

with st.sidebar:

    st.title("🧠 InsightGPT")

    st.markdown("---")

    uploaded_pdf = st.file_uploader(
        "📂 Upload Document",
        type=SUPPORTED_FILE_TYPES
    )

    st.markdown("---")

    st.subheader("🚀 Features")

    st.markdown("""
    - 📄 Document Intelligence
    - 🤖 RAG Question Answering
    - 📝 AI Summarization
    - 🔍 Semantic Search
    - 📊 Document Classification
    - 📑 Document Comparison
    - 🏢 Named Entity Recognition
    """)

    st.markdown("---")

    st.caption("Built using Gemini + ChromaDB")

# Upload Processing

if uploaded_pdf is not None:

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    with st.spinner("Processing document..."):

        file_path = save_uploaded_file(
            uploaded_pdf,
            UPLOAD_FOLDER
        )

        text, metadata = extract_text(file_path)

        st.session_state.document_text = text
        st.session_state.document_metadata = metadata

    st.success("✅ Document uploaded successfully!")

# Main Dashboard

st.title("🧠 InsightGPT")

st.caption("AI-Powered Document Intelligence Platform")

st.markdown("---")

# Display Metadata

if st.session_state.document_metadata:

    metadata = st.session_state.document_metadata

    st.subheader("📊 Document Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Pages", metadata["pages"])
    col2.metric("📝 Words", metadata["words"])
    col3.metric("🔤 Characters", metadata["characters"])
    col4.metric("📁 File", metadata["file_name"])

    st.markdown("---")
# AI Modules Layout

left, right = st.columns([2, 1])

with left:

    st.subheader("💬 Ask Questions")

    question = st.text_input(
        "Ask anything about your document..."
    )

    if st.button("🤖 Ask AI"):

        if st.session_state.document_text == "":
            st.warning("Please upload a document first.")
        else:
            st.info("RAG module will be integrated in the next milestone.")

with right:

    st.subheader("📝 AI Summary")

    if st.button("Generate Summary"):

        if st.session_state.document_text == "":
            st.warning("Please upload a document first.")
        else:
            st.info("Summarization module coming soon.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 AI Insights")

    if st.button("Extract Insights"):

        if st.session_state.document_text == "":
            st.warning("Please upload a document first.")
        else:
            st.info("NER module coming soon.")

with col2:

    st.subheader("📂 Document Classification")

    if st.button("Classify Document"):

        if st.session_state.document_text == "":
            st.warning("Please upload a document first.")
        else:
            st.info("Classification module coming soon.")

st.markdown("---")

st.subheader("📑 Compare Documents")

compare_pdf = st.file_uploader(
    "Upload Second PDF",
    type=SUPPORTED_FILE_TYPES,
    key="compare_pdf"
)

if st.button("Compare Documents"):

    if compare_pdf is None:
        st.warning("Please upload the second document.")
    else:
        st.info("Comparison module coming soon.")

st.markdown("---")

# Text Preview

if st.session_state.document_text:

    with st.expander("📖 Preview Extracted Text"):

        st.text(st.session_state.document_text[:5000])