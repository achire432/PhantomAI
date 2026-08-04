"""
MARKDOWN SERVICE
=================
Purpose: Read and process Markdown files.

Why This Matters:
- README.md files are everywhere
- Users want to read formatted markdown
- PhantomAI can explain markdown content

What It Does:
1. Reads .md files
2. Converts to HTML (for display)
3. Extracts plain text (for AI)
4. Returns both formats

How It Works:
- Uses the markdown library
- Converts to HTML
- Keeps original text

What Would Happen Without This:
- PhantomAI couldn't read README.md files
- GitHub documentation would be unreadable
- Less useful for developers
"""

import markdown
import os

def process_markdown(file_path: str) -> dict:
    """
    Read and process a markdown file.
    
    Returns:
    {
        "success": True,
        "html": "<h1>Hello</h1>",
        "raw": "# Hello",
        "file": "README.md"
    }
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert to HTML
        html = markdown.markdown(content)
        
        return {
            "success": True,
            "html": html,           # For displaying
            "raw": content,         # For AI processing
            "file": os.path.basename(file_path)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def extract_text_from_markdown(content: str) -> str:
    """
    Extract plain text from markdown content.
    
    Why This Matters:
    - AI needs plain text, not markdown symbols
    - Removes formatting symbols
    - Keeps the actual content
    
    Example:
        Input: "# Hello *world*"
        Output: "Hello world"
    """
    try:
        # Convert to HTML
        html = markdown.markdown(content)
        
        # Remove HTML tags (simple approach)
        import re
        plain_text = re.sub(r'<[^>]+>', '', html)
        
        return plain_text.strip()
        
    except Exception as e:
        return f"Error extracting text: {str(e)}"