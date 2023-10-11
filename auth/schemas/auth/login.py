from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    phone: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str