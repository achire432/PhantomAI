from fastapi import APIRouter, Depends
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.api_key_service import APIKeyManager

router = APIRouter(prefix="/api-keys", tags=["API Keys"])

@router.get("/status")
def get_api_key_status(current_user: User = Depends(get_current_user)):
    return {
        "status": APIKeyManager.get_all_status(),
        "available_services": APIKeyManager.get_available_services(),
        "missing_keys": APIKeyManager.get_missing_keys()
    }