"""Ponto de entrada da aplicação FastAPI.
Execute com: uvicorn app.main:app --reload"""

from fastapi import FastAPI

from app.api.v1.router import api_router

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
) 


# Todas as rotas da v1 ficam sob /api/v1
app.include_router(api_router, prefix=settings.app_version_api)


@app.get("/", tags=["Status"])
def read_root():
    """Health check: confirma que a API está no ar."""
    return {"status": "ok", "docs": "/docs"}
