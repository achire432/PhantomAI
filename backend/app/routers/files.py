"""
FILE MANAGEMENT ROUTER
=======================
Purpose: Handle file management API requests.

Endpoints:
- GET /files/list - List directory contents
- GET /files/info - Get file info
- GET /files/search - Search files
- GET /files/size - Get folder size

Why This Matters:
- Exposes file management to users
- All requests require authentication
- Read-only operations for safety
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.file_management_service import (
    list_directory, get_file_info, search_files, get_folder_size
)

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/list")
def list_files(
    path: str = None,
    current_user: User = Depends(get_current_user)
):
    """
    List files and folders in a directory.
    
    If no path provided, lists the user's home directory.
    """
    if not path:
        path = "/Users/achiresteven"
    
    result = list_directory(path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/info")
def file_info(
    path: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information about a file.
    """
    result = get_file_info(path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/search")
def search(
    query: str,
    path: str = "/Users/achiresteven",
    current_user: User = Depends(get_current_user)
):
    """
    Search for files by name.
    """
    result = search_files(path, query)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/size")
def folder_size(
    path: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get the total size of a folder.
    """
    result = get_folder_size(path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result