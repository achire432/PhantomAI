"""
PROACTIVE ASSISTANT ROUTER
============================
Purpose: Handle proactive assistant API requests.

Endpoints:
- GET /proactive/alerts - Get current alerts
- GET /proactive/check - Check system and return alerts
- POST /proactive/clear - Clear all alerts

Why This Matters:
- Exposes proactive functionality to users
- All requests require authentication
- Users can check system health
"""

from fastapi import APIRouter, Depends
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.proactive_service import (
    check_system, get_alerts, clear_alerts
)

router = APIRouter(prefix="/proactive", tags=["Proactive"])

@router.get("/check")
def check_current_system(current_user: User = Depends(get_current_user)):
    """
    Check system and return current alerts.
    """
    alerts = check_system()
    return {
        "alerts": alerts,
        "count": len(alerts)
    }

@router.get("/alerts")
def view_alerts(current_user: User = Depends(get_current_user)):
    """
    View all current alerts.
    """
    return {
        "alerts": get_alerts(),
        "count": len(get_alerts())
    }

@router.post("/clear")
def clear_all_alerts(current_user: User = Depends(get_current_user)):
    """
    Clear all alerts.
    """
    clear_alerts()
    return {"message": "Alerts cleared successfully"}