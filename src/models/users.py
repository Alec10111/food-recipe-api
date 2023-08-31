from bson import ObjectId
from pydantic import BaseModel, Field, SecretStr, EmailStr
from src.models.utils import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    fullname: str
    email: EmailStr = Field(unique=True, index=True)
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

