import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


def get_groq_client():
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured in .env"
        )

    return Groq(api_key=GROQ_API_KEY)


def ask_about_file(
    file_name: str,
    file_text: str,
    question: str,
) -> str:

    if not file_text.strip():
        raise ValueError(
            "The file does not contain readable text."
        )

    client = get_groq_client()

    prompt = f"""
You are PhantomAI, a helpful AI assistant.

The user has provided a file named:

{file_name}

FILE CONTENT:
----------------
{file_text}
----------------

USER QUESTION:
{question}

Answer the user's question using the file content.

Rules:
1. Base your answer primarily on the file.
2. Do not invent information that is not supported by the file.
3. If the answer cannot be found in the file, clearly say so.
4. Explain the answer clearly.
5. Use simple language unless technical language is necessary.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are PhantomAI, a helpful "
                    "file-analysis assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def summarize_file(
    file_name: str,
    file_text: str,
) -> str:

    if not file_text.strip():
        raise ValueError(
            "The file does not contain readable text."
        )

    client = get_groq_client()

    prompt = f"""
You are PhantomAI.

Summarize the following file:

FILE NAME:
{file_name}

FILE CONTENT:
----------------
{file_text}
----------------

Create a useful summary.

Include:
- Main topic
- Important points
- Key facts
- Important conclusions
- Important names, dates, numbers, or terms
- A short overall summary

Do not invent information.
Only use information supported by the file.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are PhantomAI, a document "
                    "summarization assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content