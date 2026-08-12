"""
Staff authorization dependencies for PhantomAI.

Rules:
- User must be authenticated.
- User must be active.
- User must have is_staff=True.
- Optional role checks can restrict privileged endpoints.
"""

from fastapi import Depends, HTTPException, status
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User


def require_staff(
    current_user: User = Depends(get_current_user),
) -> User:
    """Allow only active staff members."""

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive.",
        )

    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff authorization required.",
        )

    return current_user


def require_admin(
    current_user: User = Depends(require_staff),
) -> User:
    """Allow only active staff administrators."""

    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator authorization required.",
        )

    return current_user