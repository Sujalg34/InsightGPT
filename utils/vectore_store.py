import chromadb

client = chromadb.PersistentClient(
    path="chromadb"
)

collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(
    chunks,
    embeddings
):

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(

        ids=ids,

        documents=chunks,

        embeddings=embeddings.tolist()

    )


def search(query_embedding):

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=5

    )

    return results