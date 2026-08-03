from llama_cpp import Llama
import time

print("=" * 60)
print("🧠 PHANTOM AI - TESTING THE BRAIN")
print("=" * 60)

# Path to your downloaded model
MODEL_PATH = "/Users/achiresteven/Desktop/models/Qwen3-4B-Q4_K_M.gguf"

print("\n📂 Loading model...")
print(f"   File: {MODEL_PATH}")
print("   This takes 30-60 seconds on first load...")

start = time.time()

# Load the model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,        # Context window (how much it remembers)
    n_threads=4,       # Use 4 CPU threads
    verbose=False      # Don't show extra messages
)

end = time.time()
print(f"\n✅ Model loaded in {end - start:.2f} seconds!")

print("\n" + "=" * 60)
print("💬 ASKING THE AI:")
print("=" * 60)

question = "Explain in one sentence:what is an AI assistnat ?"

print(f"\n❓ Question: {question}")

# Ask the question
output = llm(
    question,
    max_tokens=150,      # Max words in response
    temperature=0.7,     # Creativity (0 = factual, 1 = creative)
    echo=False          # Don't repeat the question
)

print("\n" + "=" * 60)
print("🤖 AI RESPONSE:")
print("=" * 60)
print(output["choices"][0]["text"].strip())
print("=" * 60)
print("\n✅ Test complete!")
