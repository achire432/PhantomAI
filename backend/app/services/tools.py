"""
TOOLS SERVICE
=============

External tools used by PhantomAI.

Currently:
- Web Search using DuckDuckGo
"""

from ddgs import DDGS


def search_web(query: str, max_results: int = 8) -> dict:
    """
    Search the web using DuckDuckGo.

    Returns structured results that can be used by:
    - PhantomAI
    - Web Search Tool
    - Future research features
    """

    if not query or not query.strip():
        return {
            "success": False,
            "error": "Search query cannot be empty.",
            "results": [],
        }

    query = query.strip()

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=max_results,
                )
            )

        formatted_results = []

        for result in results:
            formatted_results.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", ""),
                }
            )

        return {
            "success": True,
            "query": query,
            "count": len(formatted_results),
            "results": formatted_results,
        }

    except Exception as error:
        return {
            "success": False,
            "query": query,
            "count": 0,
            "results": [],
            "error": f"Web search failed: {str(error)}",
        }