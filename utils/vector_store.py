import chromadb
import uuid

client = chromadb.PersistentClient(
    path="chromadb"
)

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings):
    """
    Store document chunks in ChromaDB.
    """

    ids = []
    documents = []
    vectors = []
    metadatas = []

    for chunk, embedding in zip(chunks, embeddings):

        ids.append(str(uuid.uuid4()))

        documents.append(
            chunk["text"]
        )

        vectors.append(
            embedding.tolist()
        )

        metadatas.append(
            {
                "page": chunk["page_number"],
                "document": chunk["document_name"],
                "chunk_id": chunk["chunk_id"]
            }
        )

    collection.add(

        ids=ids,

        documents=documents,

        embeddings=vectors,

        metadatas=metadatas

    )


def search_chunks(
    query_embedding,
    top_k=5
):
    """
    Perform semantic search in ChromaDB.
    """

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )

    return results


def delete_collection():
    """
    Delete all stored documents.
    Useful during development.
    """

    global client
    global collection

    client.delete_collection("documents")

    collection = client.get_or_create_collection(
        name="documents"
    )