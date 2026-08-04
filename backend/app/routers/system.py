"""
SYSTEM ROUTER
==============
Purpose: Handle system information requests.

Endpoint:
- GET /system/info - Get system information

Why We Need This:
- Exposes system info to users
- Only authenticated users can access
- Returns formatted data for frontend
"""

from fastapi import APIRouter, Depends
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.system_service import get_system_info

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/info")
def system_info(current_user: User = Depends(get_current_user)):
    """Get system information."""
    return get_system_info()