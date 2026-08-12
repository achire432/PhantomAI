"""
PhantomAI Database API

Normal users:
    - Can inspect database metadata.
    - Can execute safe SELECT queries.
    - Sensitive columns remain protected.

Staff:
    - Must be authenticated.
    - Must be active.
    - Must have is_staff=True.
    - Database access is audited.

This router is intentionally read-only.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.dependencies.staff import require_staff
from backend.app.models.user import User
from backend.app.models.audit_log import AuditLog
from backend.app.services.database_service import (
    execute_query,
    get_tables,
    get_table_info,
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):
    query: str


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/database",
    tags=["Database"],
)


# ============================================================
# NORMAL USER - LIST TABLES
# ============================================================

@router.get("/tables")
def list_tables(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return available public database tables.

    Authentication required.
    """

    result = get_tables(db)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error"),
        )

    return result


# ============================================================
# NORMAL USER - TABLE INFORMATION
# ============================================================

@router.get("/table/{table_name}")
def table_info(
    table_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return information about a database table.

    Authentication required.
    """

    result = get_table_info(
        db,
        table_name,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("error"),
        )

    return result


# ============================================================
# NORMAL USER - SAFE QUERY
# ============================================================

@router.post("/query")
def run_query(
    request: QueryRequest,
    http_request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Execute a safe SELECT query.

    Normal users remain subject to the sensitive-column
    restrictions implemented by database_service.py.
    """

    result = execute_query(
        db,
        request.query,
    )

    # --------------------------------------------------------
    # Audit the request
    # --------------------------------------------------------

    audit = AuditLog(
        user_id=current_user.id,
        organization=current_user.organization,
        role=current_user.role,
        action="DATABASE_QUERY",
        query=request.query[:5000],
        success=result.get("success", False),
        ip_address=(
            http_request.client.host
            if http_request.client
            else None
        ),
    )

    db.add(audit)
    db.commit()

    # --------------------------------------------------------
    # Return error
    # --------------------------------------------------------

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error"),
        )

    return result


# ============================================================
# STAFF - STAFF DATABASE TABLES
# ============================================================

@router.get("/staff/tables")
def staff_list_tables(
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Staff-only database table listing.

    Requires:
        is_staff=True
        is_active=True
    """

    result = get_tables(db)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error"),
        )

    return {
        "success": True,
        "staff_access": True,
        "organization": current_user.organization,
        "role": current_user.role,
        "tables": result.get("tables", []),
    }


# ============================================================
# STAFF - STAFF TABLE INFORMATION
# ============================================================

@router.get("/staff/table/{table_name}")
def staff_table_info(
    table_name: str,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Staff-only table metadata.
    """

    result = get_table_info(
        db,
        table_name,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("error"),
        )

    return {
        "success": True,
        "staff_access": True,
        "organization": current_user.organization,
        "role": current_user.role,
        "table": table_name,
        "columns": result.get("columns", []),
    }


# ============================================================
# STAFF - DATABASE QUERY
# ============================================================

@router.post("/staff/query")
def staff_query(
    request: QueryRequest,
    http_request: Request,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Staff-only database query endpoint.

    IMPORTANT:
    Staff authorization does NOT disable SQL safety.

    The database service still enforces:
        - SELECT only
        - no UPDATE
        - no DELETE
        - no INSERT
        - no DROP
        - no ALTER
        - no CREATE
        - no multiple statements
        - row limits
        - sensitive-column policies
    """

    result = execute_query(
        db,
        request.query,
    )

    # --------------------------------------------------------
    # Audit staff access
    # --------------------------------------------------------

    audit = AuditLog(
        user_id=current_user.id,
        organization=current_user.organization,
        role=current_user.role,
        action="STAFF_DATABASE_QUERY",
        query=request.query[:5000],
        success=result.get("success", False),
        ip_address=(
            http_request.client.host
            if http_request.client
            else None
        ),
    )

    db.add(audit)
    db.commit()

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error"),
        )

    return {
        **result,
        "staff_access": True,
        "organization": current_user.organization,
        "role": current_user.role,
    }


# ============================================================
# STAFF - AUDIT LOGS
# ============================================================

@router.get("/staff/audit-logs")
def get_audit_logs(
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Return recent database access logs.

    Staff can see their organization's audit history.
    """

    logs = (
        db.query(AuditLog)
        .filter(
            AuditLog.organization
            == current_user.organization
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .limit(100)
        .all()
    )

    return {
        "success": True,
        "count": len(logs),
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "organization": log.organization,
                "role": log.role,
                "action": log.action,
                "query": log.query,
                "success": log.success,
                "ip_address": log.ip_address,
                "created_at": log.created_at,
            }
            for log in logs
        ],
    }