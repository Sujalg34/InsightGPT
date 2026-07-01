import fitz
import os


def save_uploaded_file(uploaded_file, upload_folder):
    """
    Save uploaded PDF locally.
    """

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_document(file_path):
    """
    Extract text page by page and build a document object.
    """

    pdf = fitz.open(file_path)

    pages = []

    total_text = ""

    for page_number, page in enumerate(pdf):

        text = page.get_text("text")

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

        total_text += text

    document = {

        "file_name": os.path.basename(file_path),

        "total_pages": len(pdf),

        "total_words": len(total_text.split()),

        "total_characters": len(total_text),

        "pages": pages

    }

    return document