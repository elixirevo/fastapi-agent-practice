from fastapi import APIRouter
from app.api.v1 import chat, users

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/v1", tags=["chat"])
api_router.include_router(users.router, prefix="/v1/users", tags=["users"])
