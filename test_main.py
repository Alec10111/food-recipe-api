from fastapi.testclient import TestClient
from pymongo.collection import Collection
from bson.objectid import ObjectId

from main import app

client = TestClient(app)

# Mocking a sample recipe document
sample_recipe = {
    "_id": "64eda1c52a4ed18f4ce23306",
    "title": "Updated recipe",
    "description": "A test recipe description",
    "ingredients": [
        {
            "ingredient_id": "ingredient_id_1",
            "quantity": "1 unit"
        }
    ],
    "steps": [
        {
            "order": 1,
            "description": "Step 1"
        }
    ]
}


def test_create_recipe():
    response = client.post("/recipes", json=sample_recipe)
    assert response.status_code == 201
    assert response.json() == sample_recipe


def test_retrieve_existing_recipe():
    recipe_id = str(sample_recipe["_id"])
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert response.json() == sample_recipe


def test_retrieve_nonexistent_recipe():
    response = client.get("/recipes/nonexistent_recipe_id")
    assert response.status_code == 404


def test_list_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_recipe():
    recipe_id = str(sample_recipe["_id"])
    updated_data = {"title": "Updated Recipe Title"}
    response = client.put(f"/recipes/{recipe_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]


def test_update_nonexistent_recipe():
    response = client.put("/recipes/nonexistent_recipe_id", json={"title": "Updated Title"})
    assert response.status_code == 404


def test_delete_existing_recipe():
    recipe_id = str(sample_recipe["_id"])
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe deleted successfully"}


def test_delete_nonexistent_recipe():
    response = client.delete("/recipes/nonexistent_recipe_id")
    assert response.status_code == 404


# Clean up after testing
def cleanup():
    recipe_id = str(sample_recipe["_id"])
    # Remove the sample recipe from the database
    # (Replace this with your actual database cleanup logic)
    recipes_collection: Collection = app.mongodb["recipes_collection"]
    recipes_collection.delete_one({"_id": ObjectId(recipe_id)})


# Run the cleanup after all tests
def pytest_sessionfinish(session, exitstatus):
    cleanup()
