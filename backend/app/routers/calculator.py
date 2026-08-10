"""
Purpose: Handle calculator API requests.

Endpoint:
- POST /calculator/calculate - Perform a mathematical calculation
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.calculator import calculate


router = APIRouter(
    prefix="/calculator",
    tags=["Calculator"]
)


class CalculatorRequest(BaseModel):
    expression: str


@router.post("/calculate")
def calculate_expression(
    data: CalculatorRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate a mathematical expression.
    """

    expression = data.expression.strip()

    if not expression:
        raise HTTPException(
            status_code=400,
            detail="Expression is required."
        )

    if len(expression) > 500:
        raise HTTPException(
            status_code=400,
            detail="Expression is too long."
        )

    result = calculate(expression)

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Unable to calculate expression."
            )
        )

    return result