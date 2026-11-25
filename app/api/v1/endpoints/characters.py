"""Rotas de busca dos personagens."""
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_character_service
from app.services.character_service import CharacterService
from app.schemas.character import Character, Region, Vision, WeaponType, FilterOptions, CharacterPage, CharacterStats
from app.core.config import settings

router = APIRouter(prefix="/characters", tags=["Personagens"])


@router.get("", response_model=CharacterPage)
def list_characters(
        region: Region | None = None,
        vision: Vision | None = None,
        weapon_type: WeaponType | None = None,
        rarity: int | None = Query(None, ge=4, le=5),
        combat_role: str | None = Query(None, max_length=settings.max_text_length, description="Busca parcial. Ex.: healer"),
        affiliation: str | None = Query(None, max_length=settings.max_text_length, description="Busca parcial. Ex.: favonius"),
        q: str | None = Query(None, max_length=settings.max_text_length, description="Busca parcial no nome ou título"),
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
        combat_role=combat_role,
        affiliation=affiliation,
        q=q,
        limit=limit,
        offset=offset,
    )

@router.get("/filters", response_model=FilterOptions)
def get_filters(
    service: CharacterService = Depends(get_character_service),
):
    """Lista os valores disponíveis para cada filtro."""
    return service.get_filter_options()

@router.get("/stats", response_model=CharacterStats)
def get_stats(
    service: CharacterService = Depends(get_character_service),
) -> CharacterStats:
    return service.get_stats()

@router.get("/{character_id}", response_model=Character)
def get_character(
    character_id: str,
    service: CharacterService = Depends(get_character_service),
):
    """Busca um personagem pelo id. Retorna 404 se não existir."""
    return service.get_character(character_id)
    