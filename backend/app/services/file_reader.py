"""
FILE READER SERVICE
====================
Purpose: Extract text from uploaded files.

What This File Does:
1. Reads PDF files and extracts text
2. Reads TXT files and extracts text
3. Reads CSV files and extracts text

Why We Need This:
- Users want to upload documents and ask questions
- The AI can only read text, not PDFs directly
- This converts files into text the AI can understand

What Would Happen If We Removed This:
- Users couldn't upload files
- Phantom AI would be text-only
- Users would have to copy-paste long documents

Which Files Use This:
- upload.py (when users upload files)
- chat.py (when users ask about uploaded files)
"""

import os
from PyPDF2 import PdfReader
import csv

def extract_text(file_path: str) -> str:
    """
    Extract text from a file.
    
    Supports:
    - PDF (.pdf)
    - Text (.txt)
    - CSV (.csv)
    
    How It Works:
    1. Checks the file extension
    2. Uses the appropriate reader
    3. Extracts and returns the text
    
    Why We Structure It This Way:
    - One function handles all file types
    - Easy to add more file types later
    - Returns clean text (not raw binary)
    """
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        # Read PDF
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    elif ext == ".txt":
        # Read text file
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    elif ext == ".csv":
        # Read CSV
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = []
            for row in reader:
                rows.append(", ".join(row))
            return "\n".join(rows)
    
    else:
        return f"Unsupported file type: {ext}"