from fastapi import status, HTTPException, Request, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from setup import users_collection
from src.auth.deps import get_current_user
from src.auth.utils import verify_password, create_access_token, create_refresh_token
from src.models.auth import TokenModel
from src.models.users import UserInDBModel

router = APIRouter(prefix="",
                   tags=["Auth"])


@router.get('/me', summary='Get details of currently logged in user', response_model=UserInDBModel)
async def get_me(user: UserInDBModel = Depends(get_current_user)):
    return user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenModel)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
