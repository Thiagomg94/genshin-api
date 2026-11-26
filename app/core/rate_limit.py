"""Limitador de requisições por IP, compartilhado pela aplicação e testes."""
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.rate_limit_enabled,
)

# Decorador que aplica o limite às rotas. shared_limit cria um balde por IP
# compartilhado entre todas as rotas decoradas (scope="api"): 60 requisições
# por minuto no total, e não 60 por rota.
limit_requests = limiter.shared_limit(settings.rate_limit, scope="api")