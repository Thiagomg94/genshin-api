"""Rotas de busca dos personagens."""
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_character_service
from app.services.character_service import CharacterService
from app.schemas.character import Character, Region, Vision, WeaponType

router = APIRouter(prefix="/characters", tags=["Personagens"])


@router.get("", response_model=list[Character])
def list_characters(
        region: Region | None = None,
        vision: Vision | None = None,
        weapon_type: WeaponType | None = None,
        rarity: int | None = Query(None, ge=4, le=5),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        service: CharacterService = Depends(get_character_service),
):
    """Lista personagens. Os filtros são opcionais e combinam entre si."""
    return service.list_characters(
        region=region,
        vision=vision,
        weapon_type=weapon_type,
        rarity=rarity,
        limit=limit,
        offset=offset,
    )


@router.get("/{character_id}", response_model=Character)
def get_character(
        character_id: str,
        service: CharacterService = Depends(get_character_service),
):
    """Busca um personagem pelo id. Retorna 404 se não existir."""
    return service.get_character(character_id)
    