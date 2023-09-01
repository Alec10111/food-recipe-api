from bson import ObjectId
from pydantic import BaseModel, Field, SecretStr, EmailStr, validator

from setup import users_collection
from src.models.utils import PyObjectId


class UserOutModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    fullname: str
    email: EmailStr = Field(unique=True, index=True)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Dolly21",
                "fullname": "Dolly Pardon"
            }
        }


class UserInDBModel(UserOutModel):
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Dolly21",
                "fullname": "Dolly Pardon",
                "email": "dollyna@gmail.com",
                "password": "notsohashed111",
            }
        }
