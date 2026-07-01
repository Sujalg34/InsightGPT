from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(

    chunk_size=800,

    chunk_overlap=150,

    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def create_chunks(document):
    """
    Create chunks while preserving page numbers.
    """

    chunks = []

    chunk_id = 0

    for page in document["pages"]:

        split_text = splitter.split_text(page["text"])

        for text in split_text:

            chunks.append({

                "chunk_id": chunk_id,

                "page_number": page["page_number"],

                "document_name": document["file_name"],

                "text": text

            })

            chunk_id += 1

    return chunks