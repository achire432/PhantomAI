"""
CODE ANALYSIS SERVICE
======================
Purpose: Analyze Python code and provide insights.

Why This Matters:
- Developers need to understand code
- PhantomAI can explain code
- Makes learning easier
"""

import ast
import os

def analyze_python_code(file_path: str) -> dict:
    """
    Analyze a Python file and extract:
    - Functions
    - Classes
    - Imports
    - Variables
    
    Returns:
    {
        "success": True,
        "filename": "main.py",
        "functions": ["get_user", "create_user"],
        "classes": ["User", "Note"],
        "imports": ["fastapi", "sqlalchemy"],
        "lines": 50
    }
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        functions = []
        classes = []
        imports = []
        lines = len(content.split('\n'))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        return {
            "success": True,
            "filename": os.path.basename(file_path),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": lines
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_function_details(file_path: str, function_name: str) -> dict:
    """
    Get details about a specific function.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                # Get line numbers
                start_line = node.lineno
                end_line = node.end_lineno
                
                # Get source code
                lines = content.split('\n')[start_line-1:end_line]
                source = '\n'.join(lines)
                
                return {
                    "success": True,
                    "name": function_name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "source": source,
                    "params": [arg.arg for arg in node.args.args]
                }
        
        return {
            "success": False,
            "error": f"Function '{function_name}' not found"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }