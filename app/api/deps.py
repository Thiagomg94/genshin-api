"""Dependências injetáveis usadas pelos endpoints."""
from functools import lru_cache

from fastapi import Depends

from app.repositories.character_repository import CharacterRepository
from app.services.character_service import CharacterService
from app.core.config import settings

# Caminho do JSON
DATA_PATH = settings.characters_data_path

@lru_cache
def get_repository() -> CharacterRepository:
    """Carrega o JSON uma única vez e reutiliza o repositório nas requisições."""
    return CharacterRepository.from_json(DATA_PATH)


def get_character_service(
        repo: CharacterRepository = Depends(get_repository),
) -> CharacterService:
    """Monta o serviço com o repositório. FastAPI encadeia as duas dependências."""
    return CharacterService(repo)