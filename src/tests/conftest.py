import faker
import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from main import app
from setup import users_collection, recipes_collection
from src.auth.utils import create_access_token, hash_password
from src.models.recipes import RecipeModel
from src.models.users import UserInDBModel

# Mocking a sample recipe document
SAMPLE_RECIPE = {
    "title": "Sample Recipe",
    "description": "test",
    "ingredients": [{
        "name": "Pasta",
        "quantity": "1 unit"
    }],
    "steps": [{
        "order": 1,
        "description": "Boil water"
    }],
}

# Mocking a sample user document
f = faker.Faker()
SAMPLE_USER = {
    "username": f.simple_profile()["username"],
    "fullname": "test",
    "email": f.email(),
    "password": hash_password("testpassword"),
}


@pytest.fixture(scope="module", autouse=True)
def api_client():
    with TestClient(app) as client:
        yield client


# Insert the sample recipe into the test collection
@pytest.fixture(scope="module")
def recipe(user):
    recipe = RecipeModel(**SAMPLE_RECIPE)
    recipe.createdBy = user["_id"]
    recipe = recipes_collection.insert_one(jsonable_encoder(recipe))
    yield recipes_collection.find_one({"_id": recipe.inserted_id})
    recipes_collection.delete_one({"_id": recipe.inserted_id})


# Insert the sample user into the test user collection
@pytest.fixture(scope="module")
def user():
    user = UserInDBModel(**SAMPLE_USER)
    user = users_collection.insert_one(jsonable_encoder(user))
    yield users_collection.find_one({"_id": user.inserted_id})
    users_collection.delete_one({"_id": user.inserted_id})


@pytest.fixture(scope="module")
def user_auth(user):
    yield user, create_access_token(user["email"])
    users_collection.delete_one({"_id": user["_id"]})


# Clean up after testing
def cleanup():
    recipes_collection.delete_many({"description": "test"})
    users_collection.delete_many({"username": "test"})


# Run the cleanup after all tests
def pytest_sessionfinish(session, exitstatus):
    cleanup()
