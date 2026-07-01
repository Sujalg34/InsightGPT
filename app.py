import os
import streamlit as st
from utils.summarizer import summarize_document

from config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    UPLOAD_FOLDER,
    SUPPORTED_FILE_TYPES
)

from utils.parser import (
    save_uploaded_file,
    extract_document
)

from utils.chunking import (
    create_chunks
)

from utils.embeddings import (
    generate_embeddings
)

from utils.vector_store import (
    store_chunks
)

# PAGE CONFIG

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# SESSION STATE

if "document" not in st.session_state:
    st.session_state.document = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "embeddings_created" not in st.session_state:
    st.session_state.embeddings_created = False

# SIDEBAR

with st.sidebar:

    st.title("🧠 InsightGPT")

    st.markdown("---")

    uploaded_pdf = st.file_uploader(
        "📂 Upload PDF",
        type=SUPPORTED_FILE_TYPES
    )

    st.markdown("---")

    st.subheader("🚀 AI Features")

    st.markdown("""
- 📄 Document Intelligence
- 💬 RAG Question Answering
- 📝 AI Summarization
- 🔍 Semantic Search
- 📊 Document Classification
- 📑 Compare Documents
- 🏢 Named Entity Recognition
""")

    st.markdown("---")

    st.caption("Powered by Gemini + ChromaDB")

# DOCUMENT PROCESSING PIPELINE

if uploaded_pdf is not None:

    with st.spinner("Processing document..."):

        file_path = save_uploaded_file(
            uploaded_pdf,
            UPLOAD_FOLDER
        )

        document = extract_document(file_path)

        chunks = create_chunks(document)

        embeddings = generate_embeddings(chunks)

        store_chunks(
            chunks,
            embeddings
        )

        st.session_state.document = document
        st.session_state.chunks = chunks
        st.session_state.embeddings_created = True

    st.success("✅ Document Processed Successfully")

# MAIN DASHBOARD

st.title("🧠 InsightGPT")

st.caption(
    "Enterprise AI Document Intelligence Platform"
)

st.markdown("---")

# DOCUMENT METADATA

if st.session_state.document is not None:

    document = st.session_state.document

    st.subheader("📊 Document Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Pages",
        document["total_pages"]
    )

    c2.metric(
        "Words",
        document["total_words"]
    )

    c3.metric(
        "Characters",
        document["total_characters"]
    )

    c4.metric(
        "Chunks",
        len(st.session_state.chunks)
    )

    st.success("✅ Embeddings Generated")

    st.markdown("---")

# AI MODULES

left, right = st.columns([2, 1])

# RAG CHAT

with left:

    st.subheader("💬 Ask InsightGPT")

    question = st.text_input(
        "Ask anything about your document..."
    )

    if st.button("🚀 Ask AI"):

        if st.session_state.document is None:
            st.warning("Please upload a document first.")

        else:
            st.info(
                "RAG Engine will be integrated in Milestone 5."
            )

# AI SUMMARY

with right:

    st.subheader("📝 AI Summary")

    if "summary" not in st.session_state:
        st.session_state.summary = ""

    if st.button(
        "Generate Summary",
        use_container_width=True
    ):

        if not st.session_state.document_uploaded:

            st.warning(
                "Please upload a document first."
            )

        else:

            with st.spinner(
                "Generating AI Summary..."
            ):

                st.session_state.summary = summarize_document(
                    st.session_state.document
                )

    if st.session_state.summary:

        st.success("✅ Summary Generated Successfully")

        st.markdown(st.session_state.summary)

        st.download_button(
            label="📥 Download Summary",
            data=st.session_state.summary,
            file_name="InsightGPT_Summary.txt",
            mime="text/plain",
            use_container_width=True
        )

# INSIGHTS
col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 AI Insights")

    if st.button("Extract Insights"):

        if st.session_state.document is None:

            st.warning(
                "Please upload a document first."
            )

        else:

            st.info(
                "NER module coming soon."
            )

with col2:

    st.subheader("📂 Classification")

    if st.button("Classify Document"):

        if st.session_state.document is None:

            st.warning(
                "Please upload a document first."
            )

        else:

            st.info(
                "Classification module coming soon."
            )

st.markdown("---")

# DOCUMENT COMPARISON

st.subheader("📑 Compare Documents")

compare_pdf = st.file_uploader(

    "Upload Second PDF",

    type=SUPPORTED_FILE_TYPES,

    key="compare_pdf"

)

if st.button("Compare Documents"):

    if compare_pdf is None:

        st.warning(
            "Please upload another document."
        )

    else:

        st.info(
            "Comparison module will be added later."
        )

st.markdown("---")

# DOCUMENT OVERVIEW

if st.session_state.document is not None:

    st.subheader("📖 Document Preview")

    preview_text = ""

    for page in st.session_state.document["pages"][:3]:

        preview_text += page["text"] + "\n\n"

    st.text_area(

        "Preview",

        preview_text[:5000],

        height=350

    )

# FOOTER

st.markdown("---")

st.caption(
    "InsightGPT • AI Powered Document Intelligence Platform"
)