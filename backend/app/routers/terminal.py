"""
TERMINAL ROUTER
================
Purpose: Handle terminal command API requests.

Endpoints:
- GET /terminal/commands - List allowed commands
- POST /terminal/run - Run a command

Why This Matters:
- Exposes terminal functionality to users
- All requests require authentication
- Commands are validated for safety
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.terminal_service import run_command, get_allowed_commands

class CommandRequest(BaseModel):
    command: str

router = APIRouter(prefix="/terminal", tags=["Terminal"])

@router.get("/commands")
def list_commands(current_user: User = Depends(get_current_user)):
    """
    List all allowed commands.
    """
    return {
        "allowed_commands": get_allowed_commands()
    }

@router.post("/run")
def execute_command(
    request: CommandRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Run a terminal command safely.
    
    Safety:
    - Only allowed commands
    - No destructive operations
    - Timed out after 30 seconds
    - All commands are logged
    """
    
    # Validate and run the command
    result = run_command(request.command)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "success": True,
        "output": result.get("output"),
        "exit_code": result.get("exit_code")
    }