from fastapi import APIRouter, Depends, HTTPException
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.app_launcher_service import launch_app, list_common_apps

router = APIRouter(prefix="/apps", tags=["Applications"])

@router.get("/list")
def list_apps(current_user: User = Depends(get_current_user)):
    """List common applications."""
    return {"apps": list_common_apps()}

@router.post("/launch")
def launch_application(
    app_name: str,
    current_user: User = Depends(get_current_user)
):
    """Launch an application."""
    result = launch_app(app_name)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result