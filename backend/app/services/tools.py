"""
TOOLS SERVICE
==============
Purpose: Give the AI the ability to use external tools (like Web Search)
"""

from ddgs import DDGS

def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo and return text results.
    
    Why this matters:
    - The AI model was trained on data up to 2023.
    - This lets it answer questions about today's news, weather, and live data.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            summary = ""
            for r in results:
                summary += f"Title: {r['title']}\nBody: {r['body']}\n\n"
            return summary.strip()
    except Exception as e:
        return f"Search failed: {e}"