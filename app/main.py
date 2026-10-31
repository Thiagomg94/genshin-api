"""Ponto de entrada da aplicação FastAPI.
Execute com: uvicorn app.main:app --reload"""

from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="API Genshin Impact",
    description="API que retorna dados sobre personagens de Genshin Impact.",
    version="0.1.0",
)


# Todas as rotas da v1 ficam sob /api/v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Status"])
def read_root():
    """Health check: confirma que a API está no ar."""
    return {"status": "ok", "docs": "/docs"}
