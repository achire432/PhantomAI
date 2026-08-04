"""
GIT SERVICE
============
Purpose: Interact with Git repositories safely.

Why This Matters:
- Developers need to manage code
- PhantomAI can help with git operations
- Makes PhantomAI a developer assistant

How It Works:
1. Runs git commands using subprocess
2. Captures the output
3. Returns the result

Safety:
- Only READ-ONLY operations
- No destructive commands (no push, force, reset)
- Commands are hardcoded for safety

What Would Happen Without This:
- PhantomAI couldn't help with code management
- Developers would need to use terminal separately
- Less integrated experience
"""

import subprocess
import os

def run_git_command(command: list, repo_path: str = ".") -> dict:
    """
    Run a git command safely.
    
    How It Works:
    1. Takes a git command (e.g., ["git", "status"])
    2. Runs it in the terminal
    3. Captures the output
    4. Returns it
    
    Returns:
    {
        "success": True,
        "output": "git output here"
    }
    """
    try:
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check if command succeeded
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout.strip()
            }
        else:
            return {
                "success": False,
                "error": result.stderr.strip()
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def git_status(repo_path: str = ".") -> dict:
    """
    Get git status.
    
    What This Shows:
    - Modified files
    - Staged files
    - Untracked files
    
    Example Output:
    "M  backend/app/main.py\n?? new_file.py"
    """
    return run_git_command(["git", "status", "--porcelain"], repo_path)

def git_log(repo_path: str = ".", limit: int = 10) -> dict:
    """
    Get git commit log.
    
    What This Shows:
    - Commit hash
    - Commit message
    - Author name
    - How long ago
    
    Example Output:
    "a1b2c3d - Fix bug (John, 2 hours ago)"
    """
    return run_git_command(
        ["git", "log", f"-{limit}", "--pretty=format:%h - %s (%an, %ar)"],
        repo_path
    )

def git_branches(repo_path: str = ".") -> dict:
    """
    Get all branches.
    
    What This Shows:
    - Current branch (with *)
    - All other branches
    
    Example Output:
    "* main\n  feature-auth\n  bugfix-login"
    """
    return run_git_command(["git", "branch"], repo_path)

def git_current_branch(repo_path: str = ".") -> dict:
    """
    Get the current branch name.
    
    This is a more specific command for getting just the branch name.
    """
    return run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_path)

def git_diff(repo_path: str = ".") -> dict:
    """
    Get current changes (diff).
    
    What This Shows:
    - What lines were added
    - What lines were removed
    
    Example Output:
    "+print('Hello')\n-print('Hi')"
    """
    return run_git_command(["git", "diff"], repo_path)

def git_remote(repo_path: str = ".") -> dict:
    """
    Get remote repository URL.
    
    What This Shows:
    - Where the code is hosted (GitHub URL)
    
    Example Output:
    "origin  https://github.com/achire432/PhantomAI.git"
    """
    return run_git_command(["git", "remote", "-v"], repo_path)