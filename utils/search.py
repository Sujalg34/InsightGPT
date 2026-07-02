from utils.embeddings import generate_query_embedding
from utils.vector_store import search_chunks


def semantic_search(query, top_k=5):
    """
    Perform semantic search on the indexed document.
    """

    query_embedding = generate_query_embedding(query)

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    search_results = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        similarity = round((1 - distance) * 100, 2)

        search_results.append({

            "page": metadata["page"],

            "document": metadata["document"],

            "chunk": document,

            "similarity": similarity

        })

    return search_results