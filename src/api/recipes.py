from typing import List

from fastapi import HTTPException, Body, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from setup import recipes_collection
from src.auth.deps import get_current_user
from src.models.recipes import RecipeModel, UpdateRecipeModel
from src.models.users import UserInDBModel

router = APIRouter(prefix="/recipes",
                   tags=["Recipes"])


@router.post("/", response_description="Create a new recipe", response_model=RecipeModel)
async def create_recipe(user: UserInDBModel = Depends(get_current_user), recipe: RecipeModel = Body(...)):
    recipe.createdBy = user.id
    recipe = jsonable_encoder(recipe)
    new_recipe = recipes_collection.insert_one(recipe)
    created_recipe = recipes_collection.find_one({"_id": new_recipe.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recipe)


@router.get("/{recipe_id}", response_description="Retrieve a single recipe", response_model=RecipeModel)
async def retrieve_recipe(recipe_id: str):
    recipe = recipes_collection.find_one({"_id": recipe_id})
    if recipe is not None:
        return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")


@router.get("/", response_description="List all recipes", response_model=List[RecipeModel])
async def list_recipes(ingredients: str = ""):
    if ingredients:
        recipes = recipes_collection.find({"ingredients.name": {"$all": ingredients.split(",")}})
    else:
        recipes = recipes_collection.find()
    return list(recipes)


@router.put("/{recipe_id}", response_description="Update a recipe", response_model=RecipeModel)
async def update_recipe(recipe_id: str, user: UserInDBModel = Depends(get_current_user),
                        recipe_updates: UpdateRecipeModel = Body(...)):
    existing_recipe = recipes_collection.find_one({"_id": recipe_id})
    if existing_recipe is not None:
        if existing_recipe["createdBy"] != str(user.id):
            raise HTTPException(status_code=403, detail="You can only update recipes created by you")
        recipe_data = recipe_updates.dict(exclude_unset=True)
        if len(recipe_data) >= 1:
            recipes_collection.update_one({"_id": recipe_id}, {"$set": recipe_data})
        if (existing_recipe := recipes_collection.find_one({"_id": recipe_id})) is not None:
            return existing_recipe
    raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")


@router.delete("/{recipe_id}", response_description="Delete a recipe")
async def delete_recipe(recipe_id: str, user: UserInDBModel = Depends(get_current_user)):
    recipe = recipes_collection.find_one({"_id": recipe_id})
    if recipe is not None:
        if recipe["createdBy"] != str(user.id):
            raise HTTPException(status_code=403, detail="You can only recipes recipes created by you")

        result = recipes_collection.delete_one({"_id": recipe_id})
        if result.deleted_count == 1:
            return {"message": "Recipe deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")
