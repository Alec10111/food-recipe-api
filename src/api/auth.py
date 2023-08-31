from fastapi import status, HTTPException, Request, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from setup import users_collection
from src.auth.utils import verify_password, create_access_token, create_refresh_token
from src.models.auth import TokenModel
router = APIRouter(prefix="/auth",
                   tags=["Auth"])


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenModel)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.get(form_data.username, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
