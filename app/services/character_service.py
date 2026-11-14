"""Regras de negócio dos personagens."""
from app.repositories.character_repository import CharacterRepository
from app.schemas.character import Character, FilterOptions, Region, Vision, WeaponType
from app.core.exceptions import CharacterNotFoundError
from app.schemas.character import Character, Region, Vision, WeaponType


class CharacterService:
    """Orquestra buscas e paginação, usando o repositório para ler os dados."""

    def __init__(self, repository: CharacterRepository) -> None:
        self._repository = repository

    def list_characters(
        self,
        region: Region | None = None,
        vision: Vision | None = None,
        weapon_type: WeaponType | None = None,
        rarity: int | None = None,
        combat_role: str | None = None,
        affiliation: str | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Character]:
        """Filtra personagens e devolve só a página pedida."""
        found = self._repository.search(
            region=region,
            vision=vision,
            weapon_type=weapon_type,
            rarity=rarity,
            combat_role=combat_role,
            affiliation=affiliation,
            q=q
        )
        # Paginação: pega uma fatia da lista filtrada
        return found[offset : offset + limit]

    def get_character(self, character_id: str) -> Character:
        """Busca por ID. Devolve CharacterNotFoundError se não existir."""
        character = self._repository.get(character_id)
        if character is None:
            raise CharacterNotFoundError(character_id)
        return character

    def get_filter_options(self) -> FilterOptions:
        """Calcula os valores que existem nos dados para cada filtro."""
        return self._repository.filter_options()