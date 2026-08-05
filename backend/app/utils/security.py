"""
PHANTOMAI SECURITY UTILITIES
============================
This file handles the cryptographic security for PhantomAI.

CRITICAL BUG FIX FOR PYTHON 3.14:
---------------------------------
We use 'bcrypt_sha256' instead of standard 'bcrypt' because the 
newer versions of the bcrypt library have a version reading bug.
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

# --- CONFIGURATION ---
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- PASSWORD HASHING ---
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- JWT TOKEN MANAGEMENT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt