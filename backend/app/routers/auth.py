"""
PHANTOMAI AUTHENTICATION ROUTER
===============================
This module handles user creation (Registration) and user verification (Login).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imports from your project
from backend.app.database.database import get_db
from backend.app.models import User
from backend.app.schemas import UserCreate, UserLogin

# UPDATED IMPORT TO FIND THE NEW SECURITY FILE
from backend.app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    REGISTRATION ENDPOINT
    =====================
    Creates a new user in the database.
    """
    # 1. Check if email is already registered
    user_exists = db.query(User).filter(User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the password securely
    hashed_password = get_password_hash(user_data.password)

    # 3. Create the user object
    # CRITICAL FIX: The database column is named 'password', NOT 'password_hash'
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed_password  # <--- CHANGED TO 'password' TO MATCH YOUR DB
    )

    # 4. Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Generate a JWT token for immediate login
    access_token = create_access_token(data={"sub": new_user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    LOGIN ENDPOINT
    ==============
    Verifies user credentials and issues a JWT.
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # CRITICAL FIX: Check against the 'password' column in the DB
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}