from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from setup import users_collection
from src.auth.utils import get_hashed_password
from src.models.users import UserModel

router = APIRouter(prefix="/users",
                   tags=["User"])


# Create a new user
@router.post("/", response_description="Create a new user", response_model=UserModel)
def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = get_hashed_password(user["password"])
    new_user = users_collection.insert_one(user)
    created_user = users_collection.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


# Get user by ID
@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": user_id})
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="User not found")


# Delete user by ID
@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": user_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
