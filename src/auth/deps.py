from datetime import datetime
from fastapi import Depends, HTTPException, status
from jose import jwt
from pydantic import ValidationError

from setup import settings, users_collection
from .utils import oauth
from ..models.auth import TokenPayload
from ..models.users import UserInDBModel


async def get_current_user(token: str = Depends(oauth)) -> UserInDBModel:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = users_collection.find_one({"email": token_data.user_email})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserInDBModel(**user)
