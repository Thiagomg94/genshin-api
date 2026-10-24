""""Rotas de busca dos personagens"""
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query

from app.repositories.character_repository import CharacterRepository
from app.schemas.character import Character

# Caminho do JSON
DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "characters.json"

router = APIRouter(prefix="/characters", tags=["Personagens"])


@lru_cache
def get_repository() -> CharacterRepository:
    """Carrega o JSON uma única vez e reutiliza o repositório nas requisições."""
    return CharacterRepository.from_json(DATA_PATH)

@router.get("", response_model=list[Character])
def list_characters(
        region: str | None = None,
        vision: str | None = None,
        weapon_type: str | None = None,
        rarity: int | None = Query(None, ge=4, le=5),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        repo: CharacterRepository = Depends(get_repository),
):
    """Lista personagens. Os filtros são opcionais e combinam entre si."""
    found = repo.search(region=region, vision=vision, weapon_type=weapon_type, rarity=rarity)
    # Paginação
    return found[offset: offset + limit]


@router.get("/{character_id}", response_model=Character)
def get_character(
        character_id: str,
        repo: CharacterRepository = Depends(get_repository),
):
    """Busca um personagem pelo id."""
    character = repo.get(character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Personagem não encontrado.")
    return character