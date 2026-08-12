"""
Staff and role authorization dependencies.

These dependencies sit on top of JWT authentication.

Authentication:
    "Who are you?"

Authorization:
    "Are you allowed to perform this operation?"
"""

from fastapi import Depends, HTTPException, status

from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User


# ============================================================
# STAFF ACCESS
# ============================================================

def require_staff(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Require an authenticated active staff account.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive."
        )

    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff authorization required."
        )

    return current_user


# ============================================================
# ROLE ACCESS
# ============================================================

def require_roles(*allowed_roles: str):
    """
    Require the authenticated user to have one of the
    specified roles.

    Example:

        Depends(require_roles("admin", "supervisor"))
    """

    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive."
            )

        if not current_user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Staff authorization required."
            )

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges."
            )

        return current_user

    return dependency