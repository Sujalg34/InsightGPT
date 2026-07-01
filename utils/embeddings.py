from sentence_transformers import SentenceTransformer

# Load embedding model only once
embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embeddings(chunks):
    """
    Generate embeddings for all document chunks.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings


def generate_query_embedding(query):
    """
    Generate embedding for user's question.
    """

    embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding