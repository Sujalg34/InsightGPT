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

from utils.rag import (
    generate_answer
)

from utils.summarizer import (
    summarize_document
)

from utils.classifier import (
    classify_document
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "document" not in st.session_state:
    st.session_state.document = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "classification_result" not in st.session_state:
    st.session_state.classification_result = ""

if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = ""

if "rag_sources" not in st.session_state:
    st.session_state.rag_sources = []

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🧠 InsightGPT")

    st.markdown("---")

    uploaded_pdf = st.file_uploader(
        "📂 Upload PDF",
        type=SUPPORTED_FILE_TYPES
    )

    st.markdown("---")

    st.subheader("🚀 AI Modules")

    st.markdown("""
✅ RAG Question Answering

✅ AI Summarization

✅ Document Classification

🚧 Named Entity Recognition

🚧 Document Comparison

🚧 Semantic Search
""")

    st.markdown("---")

    st.caption(
        "Powered by Gemini 2.5 Flash + ChromaDB"
    )

# ==========================================================
# DOCUMENT PROCESSING
# ==========================================================

if uploaded_pdf is not None:

    with st.spinner("Processing document..."):

        file_path = save_uploaded_file(
            uploaded_pdf,
            UPLOAD_FOLDER
        )

        document = extract_document(
            file_path
        )

        chunks = create_chunks(
            document
        )

        embeddings = generate_embeddings(
            chunks
        )

        store_chunks(
            chunks,
            embeddings
        )

        st.session_state.document = document
        st.session_state.chunks = chunks
        st.session_state.document_uploaded = True

    st.success(
        "✅ Document indexed successfully!"
    )

# ==========================================================
# MAIN DASHBOARD
# ==========================================================

st.title("🧠 InsightGPT")

st.caption(
    "Enterprise AI Document Intelligence Platform"
)

st.markdown("---")

# ==========================================================
# DOCUMENT STATISTICS
# ==========================================================

if st.session_state.document_uploaded:

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

    st.success(
        "✅ Embeddings generated successfully."
    )

st.markdown("---")

# ==========================================================
# TOP AI MODULES
# ==========================================================

left, right = st.columns([2, 1])

# ==========================================================
# RAG QUESTION ANSWERING
# ==========================================================

with left:

    st.subheader("💬 Ask InsightGPT")

    question = st.text_input(
        "Ask anything about your document..."
    )

    if st.button(
        "🚀 Ask AI",
        use_container_width=True
    ):

        if not st.session_state.document_uploaded:

            st.warning(
                "Please upload a document first."
            )

        elif question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching document..."
            ):

                result = generate_answer(
                    question
                )

                st.session_state.rag_answer = result["answer"]
                st.session_state.rag_sources = result["sources"]

    if st.session_state.rag_answer:

        st.success("Answer")

        st.markdown(
            st.session_state.rag_answer
        )

        pages = sorted(
            list(
                set(
                    source["page"]
                    for source in st.session_state.rag_sources
                )
            )
        )

        st.info(
            "📚 Source Pages : "
            + ", ".join(
                map(str, pages)
            )
        )

# ==========================================================
# AI SUMMARY
# ==========================================================

with right:

    st.subheader("📝 AI Summary")

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

        st.success(
            "✅ Summary Generated Successfully"
        )

        st.markdown(
            st.session_state.summary
        )

        st.download_button(
            label="📥 Download Summary",
            data=st.session_state.summary,
            file_name="InsightGPT_Summary.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")

# ==========================================================
# AI MODULES
# ==========================================================

col1, col2 = st.columns(2)

# ==========================================================
# AI INSIGHTS (NER)
# ==========================================================

with col1:

    st.subheader("📊 AI Insights")

    if st.button(
        "Extract Insights",
        use_container_width=True
    ):

        if not st.session_state.document_uploaded:

            st.warning(
                "Please upload a document first."
            )

        else:

            st.info(
                "Named Entity Recognition module will be added in the next feature."
            )

# ==========================================================
# DOCUMENT CLASSIFICATION
# ==========================================================

with col2:

    st.subheader("📂 AI Document Classification")

    if st.button(
        "Classify Document",
        use_container_width=True
    ):

        if not st.session_state.document_uploaded:

            st.warning(
                "Please upload a document first."
            )

        else:

            with st.spinner(
                "Analyzing document..."
            ):

                st.session_state.classification_result = classify_document(
                    st.session_state.document
                )

    if st.session_state.classification_result:

        st.success(
            "✅ Classification Completed"
        )

        st.markdown(
            st.session_state.classification_result
        )

        st.download_button(
            label="📥 Download Classification",
            data=st.session_state.classification_result,
            file_name="InsightGPT_Classification.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")

# ==========================================================
# DOCUMENT COMPARISON
# ==========================================================

st.subheader("📑 Compare Documents")

compare_pdf = st.file_uploader(
    "Upload Second PDF",
    type=SUPPORTED_FILE_TYPES,
    key="compare_pdf"
)

if st.button(
    "Compare Documents",
    use_container_width=True
):

    if compare_pdf is None:

        st.warning(
            "Please upload a second document."
        )

    else:

        st.info(
            "AI Document Comparison will be implemented in the next feature."
        )

st.markdown("---")

# ==========================================================
# DOCUMENT PREVIEW
# ==========================================================

if st.session_state.document_uploaded:

    st.subheader("📖 Document Preview")

    preview_text = ""

    for page in st.session_state.document["pages"]:

        preview_text += page["text"] + "\n\n"

        if len(preview_text) >= 5000:
            break

    st.text_area(
        "Extracted Text",
        preview_text[:5000],
        height=350
    )

    with st.expander("📋 Chunk Information"):

        st.metric(
            "Total Chunks",
            len(st.session_state.chunks)
        )

        if len(st.session_state.chunks) > 0:

            first_chunk = st.session_state.chunks[0]

            st.markdown("### First Chunk")

            st.code(
                first_chunk["text"][:700]
            )

            st.markdown("### Metadata")

            st.json({
                "Chunk ID": first_chunk["chunk_id"],
                "Page": first_chunk["page_number"],
                "Document": first_chunk["document_name"]
            })

st.markdown("---")

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "🧠 InsightGPT • Enterprise AI Document Intelligence Platform"
)