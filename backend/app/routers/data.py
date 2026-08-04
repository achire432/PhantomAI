from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.data_service import export_user_data, import_user_data

class ImportData(BaseModel):
    data: dict

router = APIRouter(prefix="/data", tags=["Data"])

@router.get("/export")
def export_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export all user data as JSON.
    """
    return export_user_data(db, current_user.id)

@router.post("/import")
def import_data(
    import_data: ImportData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Import user data from JSON.
    """
    result = import_user_data(db, current_user.id, import_data.data)
    return {
        "message": "Data imported successfully",
        "imported": result
    }