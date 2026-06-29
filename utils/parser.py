import fitz
import os

def save_uploaded_file(uploaded_file, upload_folder):

    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text(file_path):

    doc = fitz.open(file_path)

    full_text = ""

    metadata = {
        "pages": len(doc),
        "file_name": os.path.basename(file_path)
    }

    for page in doc:

        full_text += page.get_text()

    metadata["characters"] = len(full_text)

    metadata["words"] = len(full_text.split())

    return full_text, metadata