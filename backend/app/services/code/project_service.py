"""
PHANTOM AI PROJECT SERVICE
==========================

Provides safe project-level file operations.

This is the foundation for PhantomAI's
Claude/Lovable-style project engine.

Responsibilities:

- Create projects
- List projects
- Inspect project trees
- Read files
- Write files
- Delete files
- Rename files
- Apply multiple changes
- Prevent path traversal outside the project workspace
"""

import os
import shutil
from pathlib import Path
from typing import Optional


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[4]

PROJECTS_DIR = BASE_DIR / "projects"

PROJECTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# PROJECT NAME VALIDATION
# ============================================================

def validate_project_name(name: str) -> bool:

    if not name:
        return False

    if len(name) > 100:
        return False

    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "-_"
    )

    return all(
        character in allowed
        for character in name
    )


# ============================================================
# GET PROJECT PATH
# ============================================================

def get_project_path(
    project_name: str,
) -> Path:

    if not validate_project_name(project_name):

        raise ValueError(
            "Invalid project name."
        )

    project_path = (
        PROJECTS_DIR /
        project_name
    ).resolve()

    if PROJECTS_DIR.resolve() not in project_path.parents:

        raise ValueError(
            "Invalid project path."
        )

    return project_path


# ============================================================
# SAFE PROJECT FILE PATH
# ============================================================

def get_safe_file_path(
    project_name: str,
    relative_path: str,
) -> Path:

    project_path = get_project_path(
        project_name
    )

    if not relative_path:
        raise ValueError(
            "File path cannot be empty."
        )

    file_path = (
        project_path /
        relative_path
    ).resolve()

    if file_path != project_path and project_path not in file_path.parents:

        raise ValueError(
            "File path escapes project directory."
        )

    return file_path


# ============================================================
# CREATE PROJECT
# ============================================================

def create_project(
    name: str,
    description: str = "",
) -> dict:

    project_path = get_project_path(
        name
    )

    if project_path.exists():

        return {
            "success": False,
            "error": "Project already exists.",
        }

    project_path.mkdir(
        parents=True,
        exist_ok=False,
    )

    readme = project_path / "README.md"

    readme.write_text(
        f"# {name}\n\n"
        f"{description}\n",
        encoding="utf-8",
    )

    return {
        "success": True,
        "name": name,
        "path": str(project_path),
        "description": description,
    }


# ============================================================
# LIST PROJECTS
# ============================================================

def list_projects() -> dict:

    projects = []

    for item in PROJECTS_DIR.iterdir():

        if not item.is_dir():
            continue

        projects.append(
            {
                "name": item.name,
                "path": str(item),
            }
        )

    projects.sort(
        key=lambda item: item["name"].lower()
    )

    return {
        "success": True,
        "count": len(projects),
        "projects": projects,
    }


# ============================================================
# PROJECT TREE
# ============================================================

def get_project_tree(
    project_name: str,
) -> dict:

    project_path = get_project_path(
        project_name
    )

    if not project_path.exists():

        return {
            "success": False,
            "error": "Project not found.",
        }

    tree = []

    for root, dirs, files in os.walk(
        project_path
    ):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in {
                ".git",
                ".venv",
                "__pycache__",
                "node_modules",
                ".idea",
                ".vscode",
            }
        ]

        relative_root = Path(root).relative_to(
            project_path
        )

        for directory in sorted(dirs):

            relative_path = (
                relative_root /
                directory
            )

            tree.append(
                {
                    "path": str(
                        relative_path
                    ),
                    "type": "directory",
                }
            )

        for file in sorted(files):

            relative_path = (
                relative_root /
                file
            )

            full_path = (
                project_path /
                relative_path
            )

            tree.append(
                {
                    "path": str(
                        relative_path
                    ),
                    "type": "file",
                    "size": full_path.stat().st_size,
                }
            )

    return {
        "success": True,
        "project": project_name,
        "tree": tree,
    }


# ============================================================
# READ FILE
# ============================================================

def read_project_file(
    project_name: str,
    file_path: str,
) -> dict:

    try:

        path = get_safe_file_path(
            project_name,
            file_path,
        )

        if not path.exists():

            return {
                "success": False,
                "error": "File not found.",
            }

        if not path.is_file():

            return {
                "success": False,
                "error": "Path is not a file.",
            }

        content = path.read_text(
            encoding="utf-8"
        )

        return {
            "success": True,
            "project": project_name,
            "path": file_path,
            "content": content,
            "size": len(content),
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
# WRITE FILE
# ============================================================

def write_project_file(
    project_name: str,
    file_path: str,
    content: str,
) -> dict:

    try:

        path = get_safe_file_path(
            project_name,
            file_path,
        )

        project_path = get_project_path(
            project_name
        )

        if not project_path.exists():

            return {
                "success": False,
                "error": "Project not found.",
            }

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "success": True,
            "project": project_name,
            "path": file_path,
            "size": len(content),
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# DELETE FILE
# ============================================================

def delete_project_file(
    project_name: str,
    file_path: str,
) -> dict:

    try:

        path = get_safe_file_path(
            project_name,
            file_path,
        )

        if not path.exists():

            return {
                "success": False,
                "error": "File or directory not found.",
            }

        if path.is_dir():

            shutil.rmtree(path)

        else:

            path.unlink()

        return {
            "success": True,
            "project": project_name,
            "path": file_path,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# RENAME
# ============================================================

def rename_project_file(
    project_name: str,
    old_path: str,
    new_path: str,
) -> dict:

    try:

        source = get_safe_file_path(
            project_name,
            old_path,
        )

        destination = get_safe_file_path(
            project_name,
            new_path,
        )

        if not source.exists():

            return {
                "success": False,
                "error": "Source path does not exist.",
            }

        if destination.exists():

            return {
                "success": False,
                "error": "Destination already exists.",
            }

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        source.rename(
            destination
        )

        return {
            "success": True,
            "project": project_name,
            "old_path": old_path,
            "new_path": new_path,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# APPLY MULTIPLE CHANGES
# ============================================================

def apply_project_changes(
    project_name: str,
    changes: list,
) -> dict:

    results = []

    for change in changes:

        action = change.get(
            "action",
            ""
        ).lower()

        path = change.get(
            "path"
        )

        if action == "create":

            result = write_project_file(
                project_name,
                path,
                change.get(
                    "content",
                    "",
                ),
            )

        elif action == "update":

            result = write_project_file(
                project_name,
                path,
                change.get(
                    "content",
                    "",
                ),
            )

        elif action == "delete":

            result = delete_project_file(
                project_name,
                path,
            )

        elif action == "rename":

            result = rename_project_file(
                project_name,
                path,
                change.get(
                    "new_path"
                ),
            )

        else:

            result = {
                "success": False,
                "error": (
                    f"Unsupported action: {action}"
                ),
            }

        results.append(
            {
                "action": action,
                "path": path,
                "result": result,
            }
        )

    failed = [
        item
        for item in results
        if not item["result"].get(
            "success"
        )
    ]

    return {
        "success": len(failed) == 0,
        "project": project_name,
        "total_changes": len(results),
        "failed_changes": len(failed),
        "results": results,
    }