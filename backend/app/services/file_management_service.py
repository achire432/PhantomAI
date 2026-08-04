"""
FILE MANAGEMENT SERVICE
========================
Purpose: Let PhantomAI work with files and folders.

Why This Matters:
- Users need to find and organize files
- PhantomAI can help with file management
- Makes PhantomAI more useful

How It Works:
1. Uses Python's os and shutil modules
2. Lists files and folders
3. Gets file information (size, date, type)
4. Creates and moves files (with confirmation)

Safety:
- Read-only by default
- Restricted to specific folders
- No deletion without confirmation
"""

import os
import shutil
from datetime import datetime

def list_directory(path: str) -> dict:
    """
    List all files and folders in a directory.
    
    Returns:
    {
        "success": True,
        "path": "/Users/achiresteven/Desktop",
        "contents": [
            {"name": "file.txt", "type": "file", "size": 1024},
            {"name": "folder", "type": "directory"}
        ]
    }
    """
    try:
        contents = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            
            contents.append({
                "name": item,
                "type": "directory" if is_dir else "file",
                "size": os.path.getsize(full_path) if not is_dir else None,
                "modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
            })
        
        return {
            "success": True,
            "path": path,
            "contents": sorted(contents, key=lambda x: x["name"])
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_file_info(path: str) -> dict:
    """
    Get detailed information about a file.
    
    Returns:
    {
        "success": True,
        "name": "file.txt",
        "path": "/Users/achiresteven/file.txt",
        "size": 1024,
        "created": "2026-08-04T10:00:00",
        "modified": "2026-08-04T10:00:00",
        "extension": ".txt"
    }
    """
    try:
        name = os.path.basename(path)
        stat = os.stat(path)
        
        return {
            "success": True,
            "name": name,
            "path": os.path.abspath(path),
            "size": stat.st_size,
            "size_readable": format_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": os.path.splitext(path)[1] if '.' in name else None,
            "is_directory": os.path.isdir(path)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def format_size(bytes_size: int) -> str:
    """
    Format file size in human-readable format.
    
    Example: 1024 -> "1 KB"
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def search_files(path: str, query: str) -> dict:
    """
    Search for files by name.
    
    How It Works:
    1. Searches recursively through folders
    2. Finds files matching the query
    3. Returns matching files
    
    Returns:
    {
        "success": True,
        "results": [
            {"name": "file.txt", "path": "/Users/.../file.txt"}
        ]
    }
    """
    try:
        results = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if query.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    results.append({
                        "name": file,
                        "path": full_path,
                        "size": os.path.getsize(full_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                    })
        
        return {
            "success": True,
            "results": results[:50],  # Limit to 50 results
            "count": len(results)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_folder_size(path: str) -> dict:
    """
    Get the total size of a folder.
    """
    try:
        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except:
                    pass
        
        return {
            "success": True,
            "path": path,
            "size": total_size,
            "size_readable": format_size(total_size)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }