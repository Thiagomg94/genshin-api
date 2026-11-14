""""Acesso aos dados dos personagens por meio de um arquivo JSON carregado em memória"""

import json
from pathlib import Path
import unicodedata

from app.schemas.character import Character, Region, Vision, WeaponType, FilterOptions

def _normalize(text: str) -> str:
    """Remove acentos e transforma em minúsculas"""
    # NFD separa o acento das letras
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")

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
               region: Region | None = None,
               vision: Vision | None = None,
               weapon_type: WeaponType | None = None,
               rarity: int | None = None,
               combat_role: str | None = None,
               affiliation: str | None = None,
               q: str | None = None,
               ) -> list[Character]:
        """Filtra personagens. Só aplica os filtros que forem informados.

        Os filtros se combinam (E): region=Inazuma e vision=Cryo
        retorna apenas quem atende aos dois.
        """
        results = self._characters

        if region:
            results = [item for item in results if item.region == region]
        if vision:
            results = [item for item in results if item.vision == vision]
        if weapon_type:
            results = [item for item in results if item.weapon_type == weapon_type]
        if rarity:
            results = [item for item in results if item.rarity == rarity]
        if combat_role:
            term = _normalize(combat_role)
            results = [item for item in results if term in _normalize(item.combat_role)]
        if affiliation:
            term = _normalize(affiliation)
            results = [item for item in results if term in _normalize(item.affiliation)]
        if q:
            term = _normalize(q)
            results = [
                item for item in results 
                if term in _normalize(item.name) or term in _normalize(item.title)
            ]

        return results

    def filter_options(self) -> FilterOptions:
        """Calcula os valores que existem nos dados para cada filtro.

        Só entram valores com ao menos um personagem. Região, elemento e arma
        seguem a ordem em que o enum foi declarado (a ordem do jogo).
        """

        region = {c.region for c in self._characters}
        vision = {c.vision for c in self._characters}
        weapon_type = {c.weapon_type for c in self._characters}

        roles = {
            role.strip()
            for item in self._characters
            for role in item.combat_role.split("/")
        }

        return FilterOptions(
            regions=[r for r in Region if r in region],
            visions=[v for v in Vision if v in vision],
            weapon_types=[w for w in WeaponType if w in weapon_type],
            rarities=sorted({c.rarity for c in self._characters}),
            combat_roles=sorted(roles),
        )
        