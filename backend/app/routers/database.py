"""
DATABASE ROUTER
================
Purpose: Handle database query API requests.

Endpoints:
- GET /database/tables - Get all tables
- GET /database/table/{name} - Get table info
- POST /database/query - Run a SQL query

Why This Matters:
- Exposes database functionality to users
- All requests require authentication
- Read-only operations only
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.database_service import (
    execute_query, get_tables, get_table_info
)

class QueryRequest(BaseModel):
    query: str

router = APIRouter(prefix="/database", tags=["Database"])

@router.get("/tables")
def list_tables(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all tables in the database.
    
    Shows:
    - All table names
    - Ordered alphabetically
    """
    result = get_tables(db)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result

@router.get("/table/{table_name}")
def table_info(
    table_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get information about a specific table.
    
    Shows:
    - Column names
    - Data types
    - Whether nullable
    """
    result = get_table_info(db, table_name)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result

@router.post("/query")
def run_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Run a SQL query on the database.
    
    Safety:
    - Only SELECT queries allowed
    - No DELETE, DROP, UPDATE, INSERT
    - Results limited to 100 rows
    - Preview shown before execution
    """
    result = execute_query(db, request.query)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result