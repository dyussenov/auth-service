from pydantic import BaseModel, EmailStr, validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from auth.db.models import UserType
from auth.config import get_settings


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
