# Establish a connection to MongoDB
from pymongo import MongoClient
from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)

    class Config:
        case_sensitive = True


settings = Settings()

# Mongodb setup
client = MongoClient(settings.MONGO_CONNECTION_STRING)
recipes_collection = client["recipe_app_db"]["recipes"]
users_collection = client["recipe_app_db"]["users"]
