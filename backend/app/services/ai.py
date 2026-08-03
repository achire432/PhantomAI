"""
AI SERVICE
==========
Connects PhantomAI to the Qwen3-4B local AI model
"""

from llama_cpp import Llama

# Path to your AI model
MODEL_PATH = "/Users/achiresteven/Desktop/models/Qwen3-4B-Q4_K_M.gguf"

# Load the AI model
print("🧠 Loading AI model... This takes 30-60 seconds.")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    verbose=False
)
print("✅ AI model loaded successfully!")

def ask_ai(prompt: str, context: list = None) -> str:
    """
    Send a prompt to the AI and get a response.
    """
    
    # System prompt tells the AI how to behave
    system_prompt = "You are a helpful AI assistant called Phantom AI. Always give short, clear, direct answers. Do not repeat yourself. Do not ask questions. Answer in 2-3 sentences maximum."
    
    # Build the conversation
    if context:
        conversation = ""
        for msg in context:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation += f"{role}: {msg['content']}\n"
        full_prompt = system_prompt + "\n\n" + conversation + f"User: {prompt}\nAssistant:"
    else:
        full_prompt = system_prompt + "\n\n" + f"User: {prompt}\nAssistant:"
    
    # Generate response
    output = llm(
        full_prompt,
        max_tokens=100,          # Shorter responses
        temperature=0.5,         # Lower = more direct
        stop=["User:", "Assistant:", "\n\n", ". "],  # Stop at various points
        echo=False
    )
    
    return output["choices"][0]["text"].strip()