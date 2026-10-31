"Agrega todos os routers da versão 1 da API."

from fastapi import APIRouter

from app.api.v1.endpoints import characters

api_router = APIRouter()
api_router.include_router(characters.router)