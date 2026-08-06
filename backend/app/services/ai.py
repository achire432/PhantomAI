from llama_cpp import Llama
from backend.app.services.tools import search_web
import json


MODEL_PATH = "/Users/achiresteven/Desktop/models/Qwen3-4B-Q4_K_M.gguf"

print("🧠 Loading AI model... This takes 30-60 seconds.")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

print("✅ AI model loaded successfully!")


def ask_ai(prompt: str, context: list = None) -> str:
    system_prompt = """You are Phantom AI, a helpful and direct assistant.

IMPORTANT RULES:
1. Give short, clear answers.
2. Do not repeat yourself.
3. Do not ask unnecessary questions.
4. If you do not know something, say that you do not know and search the web when appropriate.

WEB SEARCH:
- If the user asks about current events, recent news, current prices, current information, or anything after 2023, search the web.
- If you do not know an answer that can be found online, search the web.
- To request a web search, respond exactly in this format:

SEARCH_REQUIRED: [search query]
"""

    if context:
        conversation = ""

        for msg in context:
            role = msg.get("role", "user")

            if role == "user":
                speaker = "User"
            else:
                speaker = "Assistant"

            content = msg.get("content", "")

            conversation += f"{speaker}: {content}\n"

        full_prompt = (
            system_prompt
            + "\n\n"
            + conversation
            + f"User: {prompt}\nAssistant:"
        )
    else:
        full_prompt = (
            system_prompt
            + "\n\n"
            + f"User: {prompt}\nAssistant:"
        )

    output = llm(
        full_prompt,
        max_tokens=150,
        temperature=0.5,
        stop=["User:", "Assistant:"],
        echo=False
    )

    response = output["choices"][0]["text"].strip()

    if response.startswith("SEARCH_REQUIRED:"):
        query = response.replace("SEARCH_REQUIRED:", "", 1).strip()

        print(f"🔍 AI wants to search for: {query}")

        try:
            search_results = search_web(query)
        except Exception as e:
            print(f"⚠️ Web search failed: {e}")
            return "I was unable to complete the web search."

        search_prompt = f"""You are Phantom AI.

Use the following web search results to answer the user's question.

SEARCH RESULTS:
{search_results}

USER QUESTION:
{prompt}

Give a clear and direct answer.
Do not mention internal search instructions.
"""

        search_output = llm(
            search_prompt,
            max_tokens=200,
            temperature=0.5,
            stop=["User:", "Assistant:"],
            echo=False
        )

        return search_output["choices"][0]["text"].strip()

    return response


def ask_structured(prompt: str) -> dict:
    json_prompt = f"""
You are a data extraction assistant.

Analyze the following text and return a JSON object.

Rules:

If it is a question:
{{"type": "question", "content": "..."}}

If it is a statement:
{{"type": "statement", "content": "..."}}

If it is a greeting:
{{"type": "greeting", "content": "..."}}

If it is a command:
{{"type": "command", "content": "..."}}

Text:
{prompt}

Return ONLY valid JSON.
"""

    output = llm(
        json_prompt,
        max_tokens=150,
        temperature=0.2,
        stop=["```"],
        echo=False
    )

    response = output["choices"][0]["text"].strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "type": "unknown",
            "content": response
        }


def test_ai():
    print("🧪 Testing Phantom AI...")

    result = ask_ai("What is Phantom AI?")

    print(f"🤖 Response: {result}")

    return result


if __name__ == "__main__":
    test_ai()