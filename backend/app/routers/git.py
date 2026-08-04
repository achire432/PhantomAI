"""
GIT ROUTER
===========
Purpose: Handle git API requests.

Endpoints:
- GET /git/status - Get git status
- GET /git/log - Get commit log
- GET /git/branches - Get all branches
- GET /git/branch - Get current branch
- GET /git/diff - Get changes
- GET /git/remote - Get remote URL

Why This Matters:
- Exposes git functionality to users
- All requests require authentication
- Safe READ-ONLY operations

What It Does:
- Each endpoint calls the corresponding service
- Returns formatted results
- Handles errors gracefully
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.git_service import (
    git_status, git_log, git_branches, git_current_branch, git_diff, git_remote
)

router = APIRouter(prefix="/git", tags=["Git"])

@router.get("/status")
def get_git_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get git status.
    
    Shows:
    - Modified files (M)
    - Staged files (A)
    - Untracked files (??)
    """
    result = git_status()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "status": result["output"],
        "has_changes": bool(result["output"])
    }

@router.get("/log")
def get_git_log(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Get commit log.
    
    Shows:
    - Commit hash
    - Commit message
    - Author
    - Time ago
    """
    result = git_log(limit=limit)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "commits": result["output"].split("\n"),
        "count": len(result["output"].split("\n")) if result["output"] else 0
    }

@router.get("/branches")
def get_git_branches(
    current_user: User = Depends(get_current_user)
):
    """
    Get all branches.
    
    Shows:
    - All branches
    - Current branch (marked with *)
    """
    result = git_branches()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "branches": result["output"].split("\n"),
        "count": len(result["output"].split("\n")) if result["output"] else 0
    }

@router.get("/branch")
def get_current_branch(
    current_user: User = Depends(get_current_user)
):
    """
    Get current branch name.
    """
    result = git_current_branch()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "branch": result["output"]
    }

@router.get("/diff")
def get_git_diff(
    current_user: User = Depends(get_current_user)
):
    """
    Get current changes.
    
    Shows:
    - What was added (+)
    - What was removed (-)
    """
    result = git_diff()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "diff": result["output"],
        "has_changes": bool(result["output"])
    }

@router.get("/remote")
def get_git_remote(
    current_user: User = Depends(get_current_user)
):
    """
    Get remote repository URL.
    
    Shows:
    - Where the code is hosted
    """
    result = git_remote()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "remote": result["output"].split("\n") if result["output"] else []
    }