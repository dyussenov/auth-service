from pydantic import BaseModel, EmailStr, validator

from auth.config import get_settings
from auth.db.models import UserType


class UserResponse(BaseModel):
    email: EmailStr
    phone: str
    name: str
    surname: str
    # user_type: UserType = UserType.individual


class SignupRequest(BaseModel):
    email: EmailStr
    phone: str
    password: str
    name: str
    surname: str
    user_type: UserType = UserType.individual

    @validator("password")
    def hash_password(cls, password):
        settings = get_settings()
        hashed_password = settings.PWD_CONTEXT.hash(password)
        return hashed_password


class SignupSuccess(BaseModel):
    message: str
