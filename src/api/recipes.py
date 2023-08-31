from typing import List

from fastapi import HTTPException, Body, Request, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from setup import recipes_collection
from src.models.recipes import RecipeModel, UpdateRecipeModel

router = APIRouter(prefix="/recipes",
                   tags=["Recipes"])


@router.post("/", response_description="Create a new recipe", response_model=RecipeModel)
async def create_recipe(request: Request, recipe: RecipeModel = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = recipes_collection.insert_one(recipe)
    created_recipe = recipes_collection.find_one({"_id": new_recipe.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recipe)


@router.get("/{recipe_id}")
async def retrieve_recipe(request: Request, recipe_id: str):
    recipe = recipes_collection.find_one({"_id": recipe_id})
    if recipe is not None:
        return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")


@router.get("/", response_description="List all recipes", response_model=List[RecipeModel])
async def list_recipes(request: Request):
    recipes = recipes_collection.find()
    return list(recipes)


@router.put("/{recipe_id}")
async def update_recipe(request: Request, recipe_id: str, recipe: UpdateRecipeModel = Body(...)):
    # TODO add check on
    recipe = {k: v for k, v in recipe.dict().items() if v is not None}
    if len(recipe) >= 1:
        update_result = recipes_collection.update_one({"_id": recipe_id}, {"$set": recipe})

        if update_result.modified_count == 1:
            if (
                    updated_recipe := recipes_collection.find_one({"_id": recipe_id})
            ) is not None:
                return updated_recipe

    if (existing_recipe := recipes_collection.find_one({"_id": recipe_id})) is not None:
        return existing_recipe

    raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")


@router.delete("/{recipe_id}")
async def delete_recipe(request: Request, recipe_id: str):
    result = recipes_collection.delete_one({"_id": recipe_id})
    if result.deleted_count == 1:
        return {"message": "Recipe deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")
