import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

PROMPT_PATH = "prompts/classification_prompt.txt"


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


CLASSIFICATION_PROMPT = load_prompt()


def classify_document(document):

    text = ""

    for page in document["pages"]:

        text += page["text"] + "\n\n"

    text = text[:25000]

    prompt = CLASSIFICATION_PROMPT.format(
        document=text
    )

    response = model.generate_content(
        prompt
    )

    return response.text