"""Ponto de entrada da aplicação FastAPI.
Executar com: uvicorn app.main:app --reload"""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.rate_limit import limiter

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
) 

register_exception_handlers(app)

# slowapi procura o limitador em app.state.limiter.
app.state.limiter = limiter
# Quando o limite é excedido, responde 429 em vez de executar a rota.
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# O middleware aplica o default_limits a todas as rotas.
app.add_middleware(SlowAPIASGIMiddleware)

# Todas as rotas da v1 ficam sob /api/v1.
app.include_router(api_router, prefix=settings.app_version_api)


@app.get("/", tags=["Status"])
def read_root():
    """Health check: confirma que a API está no ar."""
    return {"status": "ok", "docs": "/docs"}
