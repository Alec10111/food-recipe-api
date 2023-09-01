from typing import List

from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from setup import users_collection
from src.auth.deps import get_current_user
from src.auth.utils import hash_password
from src.models.users import UserInDBModel, UserOutModel

router = APIRouter(prefix="/users",
                   tags=["User"])


@router.post("/", response_description="Create a new user", response_model=UserOutModel)
def create_user(user: UserInDBModel = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = hash_password(user["password"])
    if users_collection.find_one({"email": user["email"]}):
        raise HTTPException(status_code=400, detail="User with the same email already exists")
    new_user = users_collection.insert_one(user)
    created_user = users_collection.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get("/", response_description="List all users", response_model=List[UserOutModel])
async def list_users(_user: UserInDBModel = Depends(get_current_user)):
    users = users_collection.find()
    return list(users)


@router.get("/{user_id}", response_description="Retrieve a user", response_model=UserOutModel)
async def get_user(user_id: str, _user: UserInDBModel = Depends(get_current_user)):
    if (user := users_collection.find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail="User not found")
