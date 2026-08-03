"""
AI SERVICE
==========
This is the BRAIN of Phantom AI.

What This File Does:
1. Loads the Qwen3-4B AI model
2. Sends prompts to the AI
3. Handles web search when the AI doesn't know something
4. Returns structured responses

Why We Structure It This Way:
- The AI can trigger web searches
- The AI can see conversation history (context)
- Responses are short and direct
- Everything is in one place

Which Files Use This:
- chat.py (to get AI responses)
- This is the core intelligence
"""

from llama_cpp import Llama
from backend.app.services.tools import search_web
import json

# ============================================
# 1. LOAD THE AI MODEL
# ============================================

# Path to your downloaded AI model
MODEL_PATH = "/Users/achiresteven/Desktop/models/Qwen3-4B-Q4_K_M.gguf"

print("🧠 Loading AI model... This takes 30-60 seconds.")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,          # How much the AI can "remember" in one go
    n_threads=4,         # Use 4 CPU cores
    verbose=False        # Don't print extra messages
)
print("✅ AI model loaded successfully!")


# ============================================
# 2. MAIN AI FUNCTION
# ============================================

def ask_ai(prompt: str, context: list = None) -> str:
    """
    Send a prompt to the AI and get a response.
    
    How It Works:
    1. Build a system prompt telling the AI how to behave
    2. Add conversation history (context) if available
    3. Send everything to the AI model
    4. Check if the AI wants to search the web
    5. If search is needed, search and re-ask the AI
    6. Return the final answer
    
    What Would Happen If We Removed This:
    - Phantom AI would have no intelligence
    - Users would get empty responses
    - Web search wouldn't work
    
    Parameters:
    - prompt: The user's message
    - context: Previous messages (for conversation memory)
    
    Returns:
    - The AI's response as a string
    """
    
    # ----------------------------------------
    # 2a. Build the System Prompt
    # ----------------------------------------
    
    system_prompt = """You are Phantom AI, a helpful and direct assistant.

**IMPORTANT RULES:**
1. Give short, clear answers in 1-2 sentences.
2. Do NOT repeat yourself.
3. Do NOT ask questions back.
4. If you don't know something, say "I don't know" and search.

**YOU HAVE ACCESS TO WEB SEARCH.**
- If the user asks about current events, recent news, or anything after 2023, you MUST search.
- If you don't know the answer, you MUST search.
- To trigger a search, respond EXACTLY like this:
  SEARCH_REQUIRED: [what you want to search for]
"""
    
    # ----------------------------------------
    # 2b. Add Conversation Context
    # ----------------------------------------
    
    if context:
        # Build conversation history
        conversation = ""
        for msg in context:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation += f"{role}: {msg['content']}\n"
        full_prompt = system_prompt + "\n\n" + conversation + f"User: {prompt}\nAssistant:"
    else:
        full_prompt = system_prompt + "\n\n" + f"User: {prompt}\nAssistant:"
    
    # ----------------------------------------
    # 2c. Get AI Response
    # ----------------------------------------
    
    output = llm(
        full_prompt,
        max_tokens=100,          # Short responses
        temperature=0.5,         # Balanced (factual but not robotic)
        stop=["User:", "Assistant:", "\n\n"],
        echo=False
    )
    
    response = output["choices"][0]["text"].strip()
    
    # ----------------------------------------
    # 2d. Check If AI Wants to Search
    # ----------------------------------------
    
    if response.startswith("SEARCH_REQUIRED:"):
        # Extract the search query
        query = response.replace("SEARCH_REQUIRED:", "").strip()
        print(f"🔍 AI wants to search for: {query}")
        
        # Perform the search
        search_results = search_web(query)
        
        # Re-ask the AI with search results
        search_prompt = f"""Based on these search results, answer the user's question.

Search results:
{search_results}

User's original question: {prompt}

Give a clear, direct answer in 1-2 sentences."""
        
        output = llm(
            search_prompt,
            max_tokens=150,
            temperature=0.5,
            stop=["User:", "Assistant:", "\n\n"],
            echo=False
        )
        
        return output["choices"][0]["text"].strip()
    
    # If no search is needed, return the normal response
    return response


# ============================================
# 3. STRUCTURED RESPONSE FUNCTION
# ============================================

def ask_structured(prompt: str) -> dict:
    """
    Get a structured response from the AI (JSON format).
    
    Why We Need This:
    - Makes it easier to display responses
    - Frontend can parse the JSON
    - More reliable than raw text
    
    How It Works:
    1. Sends a special prompt asking for JSON
    2. The AI returns JSON
    3. We parse and return it
    
    What Would Happen If We Removed This:
    - Responses would be plain text
    - Frontend would need to parse text manually
    - Less reliable
    
    Returns:
    - A dictionary with "type" and "content" keys
    
    Example:
    {"type": "statement", "content": "I'm Phantom AI, an assistant."}
    """
    
    json_prompt = f"""
You are a data extraction assistant.
Analyze the following text and return a JSON object.

Rules:
- If it's a question, return: {{"type": "question", "content": "..."}}
- If it's a statement, return: {{"type": "statement", "content": "..."}}
- If it's a greeting, return: {{"type": "greeting", "content": "..."}}
- If it's a command, return: {{"type": "command", "content": "..."}}

Text: {prompt}

Return ONLY valid JSON. No other text.
"""
    
    output = llm(
        json_prompt,
        max_tokens=150,
        temperature=0.2,  # Lower = more precise
        stop=["```", "\n\n"],
        echo=False
    )
    
    response = output["choices"][0]["text"].strip()
    
    # Try to parse as JSON
    try:
        return json.loads(response)
    except:
        # If JSON parsing fails, return a fallback
        return {"type": "unknown", "content": response}


# ============================================
# 4. TEST FUNCTION (For Debugging)
# ============================================

def test_ai():
    """
    Quick test function to verify the AI works.
    Run this directly to test the model.
    """
    print("🧪 Testing AI...")
    result = ask_ai("What is Phantom AI?")
    print(f"🤖 Response: {result}")
    return result

if __name__ == "__main__":
    test_ai()