from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.models.users import UserModel
from src.models.utils import PyObjectId


class IngredientModel(BaseModel):
    ingredient_id: str
    quantity: str


class StepModel(BaseModel):
    order: int
    description: str


class RecipeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    ingredients: List[IngredientModel]
    steps: List[StepModel]
    createdBy: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "title": "Test Recipe",
            "description": "A test recipe description",
            "ingredients": [
                {"ingredient_id": "ingredient_id_1", "quantity": "1 unit"}
            ],
            "steps": [
                {"order": 1, "description": "Step 1"}
            ],
            "createdBy": "64f07c2138ff21aedc4aebf2"
        }


class UpdateRecipeModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    ingredients: Optional[List[IngredientModel]]
    steps: Optional[List[StepModel]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "title": "Test Recipe",
            "description": "A test recipe description",
            "ingredients": [
                {"ingredient_id": "ingredient_id_1", "quantity": "1 unit"}
            ],
            "steps": [
                {"order": 1, "description": "Step 1"}
            ]
        }