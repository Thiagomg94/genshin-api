"""Regras de negócio dos personagens."""
from app.repositories.character_repository import CharacterRepository
from app.schemas.character import Character


class CharacterService:
    """Orquestra buscas e paginação, usando o repositório para ler os dados."""

    def __init__(self, repository: CharacterRepository) -> None:
        self._repository = repository

    def list_characters(
        self,
        region: str | None = None,
        vision: str | None = None,
        weapon_type: str | None = None,
        rarity: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Character]:
        """Filtra personagens e devolve só a página pedida."""
        found = self._repository.search(
            region=region, vision=vision, weapon_type=weapon_type, rarity=rarity
        )
        # Paginação: pega uma fatia da lista filtrada
        return found[offset : offset + limit]

    def get_character(self, character_id: str) -> Character | None:
        """Busca por ID. Devolve None se não existir."""
        return self._repository.get(character_id)