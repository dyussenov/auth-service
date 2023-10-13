from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenRequest(BaseModel):
    refresh_token: str
