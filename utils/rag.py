import os
from dotenv import load_dotenv
import google.generativeai as genai

from utils.embeddings import generate_query_embedding
from utils.vector_store import search_chunks

# ==========================================
# GEMINI CONFIGURATION
# ==========================================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================
# RAG ANSWER GENERATION
# ==========================================

def generate_answer(question):
    """
    Retrieve relevant document chunks from ChromaDB
    and generate an answer using Gemini.
    """

    # Generate embedding for the user's question
    query_embedding = generate_query_embedding(question)

    # Search ChromaDB
    results = search_chunks(
        query_embedding=query_embedding,
        top_k=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Build context
    context = ""

    sources = []

    for document, metadata in zip(documents, metadatas):

        context += f"""
Page {metadata['page']}:

{document}

"""

        sources.append(
            {
                "page": metadata["page"],
                "document": metadata["document"],
                "chunk_id": metadata["chunk_id"]
            }
        )

    prompt = f"""
You are InsightGPT, an AI-powered Document Intelligence Assistant.

Answer ONLY from the provided document context.

If the answer is not available in the context, reply exactly:

"I could not find the answer in the uploaded document."

==========================
DOCUMENT CONTEXT
==========================

{context}

==========================
QUESTION
==========================

{question}

==========================
ANSWER
==========================
"""

    response = model.generate_content(prompt)

    return {
        "answer": response.text,
        "sources": sources
    }