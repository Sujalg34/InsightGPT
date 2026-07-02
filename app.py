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

from utils.ner import (
    extract_entities
)

from utils.comparision import (
    compare_documents
)

from utils.search import (
    semantic_search
)

from utils.vector_store import (
    delete_collection
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

if "entities" not in st.session_state:
    st.session_state.entities = ""

if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = ""
    
if "semantic_results" not in st.session_state:
    st.session_state.semantic_results = []

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🧠 InsightGPT")

    st.caption(
        "Enterprise AI Document Intelligence Platform"
    )

    st.markdown("---")

    uploaded_pdf = st.file_uploader(
        "📂 Upload PDF",
        type=SUPPORTED_FILE_TYPES
    )

    st.markdown("---")

    st.subheader("🚀 AI Features")

    st.success("✅ RAG Question Answering")
    st.success("✅ AI Summarization")
    st.success("✅ Document Classification")
    st.success("✅ Named Entity Recognition")
    st.success("✅ Document Comparison")
    st.success("✅ Semantic Search")

    st.markdown("---")

    st.subheader("📊 Current Status")

    if st.session_state.document_uploaded:

        st.success("Document Indexed")

        st.metric(
            "Chunks",
            len(st.session_state.chunks)
        )

    else:

        st.warning("No Document Uploaded")

    st.markdown("---")

    st.subheader("⚙️ Project")

    st.markdown("""
**Model**
- Gemini 2.5 Flash

**Embeddings**
- BAAI/bge-small-en-v1.5

**Vector Database**
- ChromaDB

**Framework**
- Streamlit
""")

    st.markdown("---")

st.subheader("🛠 Maintenance")

if st.button(
    "🗑 Clear Database",
    use_container_width=True
):

    delete_collection()

    st.success(
        "Vector database cleared."
    )

if st.button(
    "🔄 Reset Session",
    use_container_width=True
):

    keys = list(st.session_state.keys())

    for key in keys:

        del st.session_state[key]

    st.rerun()

    st.markdown("---")

    st.caption(
        "Version 1.0"
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

st.markdown(
    """
### Enterprise AI Document Intelligence Platform

Analyze documents using **Large Language Models**, **Retrieval-Augmented Generation (RAG)**, **Semantic Search**, and **Generative AI**.

Upload a PDF to begin.
"""
)

st.markdown("---")

# ==========================================================
# DOCUMENT STATISTICS
# ==========================================================

if st.session_state.document_uploaded:

    document = st.session_state.document

    st.subheader("📊 Document Statistics")

    c1, c2, c3, c4, c5 = st.columns(4)

    c1.metric(
    "📄 Pages",
    document["total_pages"]
    )

    c2.metric(
        "📝 Words",
        document["total_words"]
    )

    c3.metric(
        "🔤 Characters",
        document["total_characters"]
    )

    c4.metric(
        "🧩 Chunks",
        len(st.session_state.chunks)
    )

    c5.metric(
        "🤖 AI Modules",
        "6"
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

            with st.spinner(
                "Extracting entities..."
            ):

                st.session_state.entities = extract_entities(
                    st.session_state.document
                )

    if st.session_state.entities:

        st.success(
            "✅ AI Insights Generated"
        )

        st.markdown(
            st.session_state.entities
        )

        st.download_button(
            label="📥 Download Insights",
            data=st.session_state.entities,
            file_name="InsightGPT_Insights.txt",
            mime="text/plain",
            use_container_width=True
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

st.subheader("📑 AI Document Comparison")

compare_pdf = st.file_uploader(
    "Upload Second PDF",
    type=SUPPORTED_FILE_TYPES,
    key="compare_pdf"
)

if st.button(
    "Compare Documents",
    use_container_width=True
):

    if not st.session_state.document_uploaded:

        st.warning(
            "Please upload the first document."
        )

    elif compare_pdf is None:

        st.warning(
            "Please upload the second document."
        )

    else:

        with st.spinner(
            "Processing second document..."
        ):

            second_file_path = save_uploaded_file(
                compare_pdf,
                UPLOAD_FOLDER
            )

            second_document = extract_document(
                second_file_path
            )

        with st.spinner(
            "Comparing documents using Gemini..."
        ):

            st.session_state.comparison_result = compare_documents(
                st.session_state.document,
                second_document
            )

if st.session_state.comparison_result:

    st.success(
        "✅ Comparison Completed"
    )

    st.markdown(
        st.session_state.comparison_result
    )

    st.download_button(
        label="📥 Download Comparison Report",
        data=st.session_state.comparison_result,
        file_name="InsightGPT_Comparison.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==========================================================
# SEMANTIC SEARCH
# ==========================================================

st.markdown("---")

st.subheader("🔍 Semantic Search")

search_query = st.text_input(
    "Search by meaning instead of keywords..."
)

if st.button(
    "Search Document",
    use_container_width=True
):

    if not st.session_state.document_uploaded:

        st.warning(
            "Please upload a document first."
        )

    elif search_query.strip() == "":

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner(
            "Searching document..."
        ):

            st.session_state.semantic_results = semantic_search(
                search_query,
                top_k=5
            )

if st.session_state.semantic_results:

    st.success(
        f"Found {len(st.session_state.semantic_results)} relevant chunks"
    )

    for index, result in enumerate(
        st.session_state.semantic_results,
        start=1
    ):

        with st.expander(
            f"Result {index} • Page {result['page']} • Similarity {result['similarity']}%"
        ):

            st.markdown(
                f"**Document:** {result['document']}"
            )

            st.markdown(
                f"**Similarity Score:** {result['similarity']}%"
            )

            st.markdown("---")

            st.write(
                result["chunk"]
            )

# ==========================================================
# EXPORT CENTER
# ==========================================================

st.markdown("---")

st.subheader("📤 Export AI Results")

col1, col2 = st.columns(2)

with col1:

    if st.session_state.get("summary", ""):

        st.download_button(
            label="📥 Summary",
            data=st.session_state.summary,
            file_name="InsightGPT_Summary.txt",
            mime="text/plain",
            use_container_width=True
        )

    if st.session_state.get("classification_result", ""):

        st.download_button(
            label="📥 Classification",
            data=st.session_state.classification_result,
            file_name="InsightGPT_Classification.txt",
            mime="text/plain",
            use_container_width=True
        )

with col2:

    if st.session_state.get("entities", ""):

        st.download_button(
            label="📥 AI Insights",
            data=st.session_state.entities,
            file_name="InsightGPT_Insights.txt",
            mime="text/plain",
            use_container_width=True
        )

    if st.session_state.get("comparison_result", ""):

        st.download_button(
            label="📥 Comparison",
            data=st.session_state.comparison_result,
            file_name="InsightGPT_Comparison.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==========================================================
# DOCUMENT PREVIEW
# ==========================================================

if st.session_state.document_uploaded:

    st.markdown("---")

    st.subheader("📖 Document Preview")

    preview = ""

    for page in st.session_state.document["pages"]:

        preview += page["text"] + "\n\n"

        if len(preview) >= 5000:
            break

    st.text_area(
        "Extracted Text",
        preview[:5000],
        height=350
    )

    with st.expander("📋 Document Information"):

        st.write(
            f"**Document:** {st.session_state.document['file_name']}"
        )

        st.write(
            f"**Pages:** {st.session_state.document['total_pages']}"
        )

        st.write(
            f"**Chunks:** {len(st.session_state.chunks)}"
        )

        st.write(
            f"**Words:** {st.session_state.document['total_words']}"
        )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
"""
<div style="text-align:center">

### 🧠 InsightGPT

Enterprise AI Document Intelligence Platform

Built using

**Streamlit • Gemini 2.5 Flash • ChromaDB • Sentence Transformers • Python**

Version 1.0

</div>
""",
unsafe_allow_html=True
)