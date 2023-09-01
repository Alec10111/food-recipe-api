from src.tests.conftest import *

client = TestClient(app)


def test_create_recipe_unauthorized():
    response = client.post("/recipes", json=SAMPLE_RECIPE)
    assert response.status_code == 401


def test_create_recipe(user_auth):
    _, token = user_auth
    response = client.post("/recipes", json=SAMPLE_RECIPE, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201


def test_retrieve_existing_recipe(user_auth, recipe):
    _, token = user_auth
    response = client.get(f"/recipes/{recipe['_id']}")
    assert response.status_code == 200


def test_retrieve_nonexistent_recipe():
    response = client.get("/recipes/nonexistent_recipe_id")
    assert response.status_code == 404


def test_list_recipes(recipe):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_filter_list_recipes_negative(recipe):
    response = client.get("/recipes?ingredients=randomIngredient")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_filter_list_recipes(recipe):
    ingredient = recipe["ingredients"][0]["name"]
    response = client.get(f"/recipes?ingredients={ingredient}")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_recipe(recipe):
    user = users_collection.find_one({"_id": recipe["createdBy"]})
    token = create_access_token(user["email"])
    updated_data = {"title": "Updated Recipe Title"}
    response = client.put(f"/recipes/{recipe['_id']}", json=updated_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]


def test_update_nonexistent_recipe(user_auth):
    _, token = user_auth
    response = client.put("/recipes/nonexistent_recipe_id",
                          json={"title": "Updated Title"},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_delete_existing_recipe(recipe):
    user = users_collection.find_one({"_id": recipe["createdBy"]})
    token = create_access_token(user["email"])
    response = client.delete(f"/recipes/{recipe['_id']}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe deleted successfully"}


def test_delete_nonexistent_recipe(user_auth):
    _, token = user_auth
    response = client.delete("/recipes/nonexistent_recipe_id", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
