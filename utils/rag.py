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

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# ==========================================
# SESSION STATE
# ==========================================

if "document" not in st.session_state:
    st.session_state.document = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

# ==========================================
# SIDEBAR
# ==========================================

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
- 💬 RAG Question Answering
- 📝 AI Summarization
- 🔍 Semantic Search
- 📊 Classification
- 📑 Compare Documents
- 🏢 Named Entity Recognition
""")

    st.markdown("---")

    st.caption("Powered by Gemini + ChromaDB")

# ==========================================
# DOCUMENT PROCESSING
# ==========================================

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

    st.success("✅ Document indexed successfully!")

# ==========================================
# MAIN PAGE
# ==========================================

st.title("🧠 InsightGPT")

st.caption(
    "AI Powered Document Intelligence Platform"
)

st.markdown("---")

# ==========================================
# DOCUMENT STATISTICS
# ==========================================

if st.session_state.document_uploaded:

    document = st.session_state.document

    st.subheader("📊 Document Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Pages",
        document["total_pages"]
    )

    col2.metric(
        "Words",
        document["total_words"]
    )

    col3.metric(
        "Characters",
        document["total_characters"]
    )

    col4.metric(
        "Chunks",
        len(st.session_state.chunks)
    )

    st.success(
        "✅ Embeddings stored successfully."
    )

    st.markdown("---")

# ==========================================
# AI CHAT (RAG)
# ==========================================

left, right = st.columns([2,1])

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
                "Thinking..."
            ):

                result = generate_answer(
                    question
                )

                st.success("Answer")

                st.write(
                    result["answer"]
                )

                st.markdown("### 📚 Sources")

                pages = sorted(
                    list(
                        set(
                            source["page"]
                            for source in result["sources"]
                        )
                    )
                )

                st.info(
                    "Referenced Pages: "
                    + ", ".join(
                        str(page)
                        for page in pages
                    )
                )

# ==========================================
# AI SUMMARY
# ==========================================

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

            st.info(
                "Summarization will be added in Milestone 6."
            )

st.markdown("---")

# ==========================================
# AI MODULES
# ==========================================

col1, col2 = st.columns(2)

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
                "Named Entity Recognition module will be added later."
            )

with col2:

    st.subheader("📂 Document Classification")

    if st.button(
        "Classify Document",
        use_container_width=True
    ):

        if not st.session_state.document_uploaded:

            st.warning(
                "Please upload a document first."
            )

        else:

            st.info(
                "Classification module will be added later."
            )

st.markdown("---")

# ==========================================
# DOCUMENT COMPARISON
# ==========================================

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
            "Please upload another document."
        )

    else:

        st.info(
            "Document comparison will be added in a later milestone."
        )

st.markdown("---")

# ==========================================
# DOCUMENT PREVIEW
# ==========================================

if st.session_state.document_uploaded:

    st.subheader("📖 Document Preview")

    preview_text = ""

    for page in st.session_state.document["pages"]:

        preview_text += page["text"] + "\n\n"

        if len(preview_text) > 5000:
            break

    st.text_area(
        "Extracted Text",
        preview_text[:5000],
        height=350
    )

    with st.expander("📋 Chunk Information"):

        st.write(
            f"Total Chunks Created: {len(st.session_state.chunks)}"
        )

        if len(st.session_state.chunks) > 0:

            first_chunk = st.session_state.chunks[0]

            st.markdown("**First Chunk Preview**")

            st.code(
                first_chunk["text"][:800]
            )

            st.markdown("**Metadata**")

            st.json(
                {
                    "Chunk ID": first_chunk["chunk_id"],
                    "Page": first_chunk["page_number"],
                    "Document": first_chunk["document_name"]
                }
            )

st.markdown("---")

# ==========================================
# FOOTER
# ==========================================

st.caption(
    "🧠 InsightGPT | AI-Powered Document Intelligence Platform | Built with Streamlit, Gemini & ChromaDB"
)