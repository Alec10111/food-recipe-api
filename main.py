import uvicorn
from fastapi import FastAPI, APIRouter
from src.api import users, recipes, auth

app = FastAPI()

router = APIRouter()
router.include_router(users.router)
router.include_router(recipes.router)
router.include_router(auth.router)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
