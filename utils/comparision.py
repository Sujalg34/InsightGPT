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

PROMPT_PATH = "prompts/comparison_prompt.txt"


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


COMPARISON_PROMPT = load_prompt()


def compare_documents(document1, document2):

    text1 = ""
    text2 = ""

    for page in document1["pages"]:
        text1 += page["text"] + "\n\n"

    for page in document2["pages"]:
        text2 += page["text"] + "\n\n"

    text1 = text1[:20000]
    text2 = text2[:20000]

    prompt = COMPARISON_PROMPT.format(
        document1=text1,
        document2=text2
    )

    response = model.generate_content(
        prompt
    )

    return response.text