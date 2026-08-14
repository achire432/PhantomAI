"""
PHANTOM AI UNIVERSAL CODE ANALYZER
===================================

Universal entry point for PhantomAI's Code Engine.

Responsibilities:
- Detect programming language
- Read source files
- Extract basic structural information
- Detect syntax errors where Python AST is available
- Return a unified analysis structure
- Prepare code for AI-powered analysis

This module does NOT generate or modify code.
"""

import ast
import os
from typing import Optional


# ============================================================
# LANGUAGE REGISTRY
# ============================================================

LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".dart": "dart",
    ".scala": "scala",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".sql": "sql",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".vue": "vue",
    ".xml": "xml",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
}


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(file_path: str) -> Optional[str]:
    """
    Detect language from file extension.
    """

    extension = os.path.splitext(file_path)[1].lower()

    return LANGUAGE_EXTENSIONS.get(extension)


# ============================================================
# READ SOURCE FILE
# ============================================================

def read_source_file(file_path: str) -> dict:
    """
    Safely read a source file.
    """

    try:

        if not os.path.isfile(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}",
            }

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            content = file.read()

        return {
            "success": True,
            "content": content,
        }

    except UnicodeDecodeError:

        return {
            "success": False,
            "error": "File is not valid UTF-8 text.",
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# BASIC FILE INFORMATION
# ============================================================

def get_file_information(file_path: str) -> dict:
    """
    Return language-independent file information.
    """

    result = read_source_file(file_path)

    if not result["success"]:
        return result

    content = result["content"]

    language = detect_language(file_path)

    return {
        "success": True,
        "filename": os.path.basename(file_path),
        "path": os.path.abspath(file_path),
        "language": language or "unknown",
        "extension": os.path.splitext(file_path)[1].lower(),
        "lines": len(content.splitlines()),
        "characters": len(content),
        "empty": not bool(content.strip()),
    }


# ============================================================
# PYTHON ANALYSIS
# ============================================================

def analyze_python(
    content: str,
) -> dict:
    """
    Analyze Python source using the built-in AST parser.
    """

    try:

        tree = ast.parse(content)

    except SyntaxError as error:

        return {
            "success": False,
            "syntax_error": {
                "type": "SyntaxError",
                "message": error.msg,
                "line": error.lineno,
                "column": error.offset,
                "text": error.text.strip()
                if error.text
                else None,
            },
            "functions": [],
            "classes": [],
            "imports": [],
            "variables": [],
        }

    functions = []
    classes = []
    imports = []
    variables = []

    for node in ast.walk(tree):

        # ----------------------------------------------------
        # FUNCTIONS
        # ----------------------------------------------------

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            functions.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                    "async": isinstance(
                        node,
                        ast.AsyncFunctionDef,
                    ),
                    "parameters": [
                        arg.arg
                        for arg in node.args.args
                    ],
                }
            )

        # ----------------------------------------------------
        # CLASSES
        # ----------------------------------------------------

        elif isinstance(
            node,
            ast.ClassDef,
        ):

            classes.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                }
            )

        # ----------------------------------------------------
        # IMPORT
        # ----------------------------------------------------

        elif isinstance(
            node,
            ast.Import,
        ):

            for alias in node.names:

                imports.append(
                    alias.name
                )

        # ----------------------------------------------------
        # FROM IMPORT
        # ----------------------------------------------------

        elif isinstance(
            node,
            ast.ImportFrom,
        ):

            if node.module:
                imports.append(
                    node.module
                )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        elif isinstance(
            node,
            ast.Assign,
        ):

            for target in node.targets:

                if isinstance(
                    target,
                    ast.Name,
                ):

                    variables.append(
                        target.id
                    )

    return {
        "success": True,
        "syntax_error": None,
        "functions": functions,
        "classes": classes,
        "imports": sorted(
            set(imports)
        ),
        "variables": sorted(
            set(variables)
        ),
    }


# ============================================================
# GENERIC LANGUAGE ANALYSIS
# ============================================================

def analyze_generic(
    content: str,
    language: str,
) -> dict:
    """
    Basic analysis for languages that do not yet
    have a dedicated parser.
    """

    lines = content.splitlines()

    comments = 0
    blank_lines = 0

    for line in lines:

        stripped = line.strip()

        if not stripped:
            blank_lines += 1

        elif (
            stripped.startswith("//")
            or stripped.startswith("#")
            or stripped.startswith("--")
        ):
            comments += 1

    return {
        "success": True,
        "syntax_error": None,
        "functions": [],
        "classes": [],
        "imports": [],
        "variables": [],
        "comments": comments,
        "blank_lines": blank_lines,
        "parser": "generic",
        "parser_language": language,
    }


# ============================================================
# UNIVERSAL ANALYSIS ENTRY POINT
# ============================================================

def analyze_code(
    file_path: str,
) -> dict:
    """
    Main entry point for PhantomAI Code Engine.
    """

    information = get_file_information(
        file_path
    )

    if not information["success"]:
        return information

    source = read_source_file(
        file_path
    )

    content = source["content"]

    language = information["language"]

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    if language == "python":

        analysis = analyze_python(
            content
        )

        parser = "python_ast"

    # --------------------------------------------------------
    # OTHER LANGUAGES
    # --------------------------------------------------------

    else:

        analysis = analyze_generic(
            content,
            language,
        )

        parser = "generic"

    return {
        "success": True,

        "file": {
            "filename": information["filename"],
            "path": information["path"],
            "language": language,
            "extension": information["extension"],
            "lines": information["lines"],
            "characters": information["characters"],
            "empty": information["empty"],
        },

        "analysis": analysis,

        "capabilities": {
            "language_detection": True,
            "file_reading": True,
            "python_ast": language == "python",
            "syntax_detection": language == "python",
            "static_analysis": False,
            "security_analysis": False,
            "ai_analysis": False,
            "debugging": False,
            "code_generation": False,
            "code_modification": False,
            "project_generation": False,
        },

        "parser": parser,

        "message": (
            "PhantomAI universal code analysis completed."
        ),
    }
