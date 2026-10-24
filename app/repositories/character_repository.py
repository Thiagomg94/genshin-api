""""Acesso aos dados dos personagens por meio de um arquivo JSON carregado em memória"""

import json
from pathlib import Path

from app.schemas.character import Character

class CharacterRepository:
    """Guarda os personagens em memória, oferece busca e aplica filtros"""
    def __init__(self, characters: list[Character]) -> None:
        self._characters = characters
        # Dicionário id -> personagem, para busca direta sem percorrer a lista
        self._by_id = {c.id: c for c in self._characters}

    @classmethod
    def from_json(cls, path: Path) -> "CharacterRepository":
        """Lê o arquivo JSON e valida cada personagem com o schema."""
        with path.open(encoding="utf-8") as file:
            raw = json.load(file)
        return cls([Character(**item) for item in raw])

    def get(self, character_id: str) -> Character | None:
        """Retorna o personagem pelo id (sem diferenciar maiúsculas) ou None."""
        return self._by_id.get(character_id.lower())

    def search(self,
               region: str | None = None,
               vision: str | None = None,
               weapon_type: str | None = None,
               rarity: int | None = None,
               ) -> list[Character]:
        """Filtra personagens. Só aplica os filtros que forem informados.

        Os filtros se combinam (E): region=Inazuma e vision=Cryo
        retorna apenas quem atende aos dois.
        """
        results = self._characters

        if region:
            results = [item for item in results if item.region.lower() == region.lower()]
        if vision:
            results = [item for item in results if item.vision.lower() == vision.lower()]
        if weapon_type:
            results = [item for item in results if item.weapon_type.lower() == weapon_type.lower()]
        if rarity:
            results = [item for item in results if item.rarity == rarity]

        return results