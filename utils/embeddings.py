from sentence_transformers import SentenceTransformer

# Load only once
embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embeddings(chunks):

    embeddings = embedding_model.encode(
        chunks,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return embeddings