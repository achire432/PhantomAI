from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    full_name: str
    email: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
