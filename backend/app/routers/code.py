"""
CODE ANALYSIS ROUTER
=====================
Purpose: Handle code analysis API requests.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.code_analysis_service import (
    analyze_python_code,
    get_function_details
)

router = APIRouter(prefix="/code", tags=["Code"])

@router.post("/analyze")
def analyze_code(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a Python file.
    
    Shows:
    - Functions
    - Classes
    - Imports
    - Line count
    """
    result = analyze_python_code(file_path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/function")
def get_function(
    file_path: str,
    function_name: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get details about a specific function.
    """
    result = get_function_details(file_path, function_name)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error"))
    return result