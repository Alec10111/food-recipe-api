from uuid import UUID
from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    user_id: str = None
    exp: int = None
