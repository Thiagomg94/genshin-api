""""Modelos Pydantic que definem o formato de um personagem"""
from enum import Enum

from pydantic import BaseModel, Field

class CaseInsensitiveEnum(str, Enum):
    """"Enum de texto que aceita qualquer combinação de maiúsculas e minúsculas"""

    @classmethod
    def _missing_(cls, value):
        # Chamado quando o valor não é encontrado no Enum: tenta ignorando o caso
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None


class Region(CaseInsensitiveEnum):
    MONDSTADT = "Mondstadt"
    LIYUE = "Liyue"
    INAZUMA = "Inazuma"
    SUMERU = "Sumeru"
    FONTAINE = "Fontaine"
    NATLAN = "Natlan"
    NOD_KRAI = "Nod-Krai"
    SNEZHNAYA = "Snezhnaya"

class Vision(CaseInsensitiveEnum):
    ANEMO = "Anemo"
    GEO = "Geo"
    ELECTRO = "Electro"
    DENDRO = "Dendro"
    HYDRO = "Hydro"
    PYRO = "Pyro"
    CRYO = "Cryo"

class WeaponType(CaseInsensitiveEnum):
    SWORD = "Sword"
    CLAYMORE = "Claymore"
    POLEARM = "Polearm"
    BOW = "Bow"
    CATALYST = "Catalyst"
    

class Character(BaseModel):
    """"Um personagem de Genshin Impact, no mesmo modelo do JSON"""
    id: str = Field(description="Identificar único, ex.: hu-tao")
    name: str
    title: str
    vision: Vision
    weapon_type: WeaponType
    rarity: int
    combat_role: str
    region: Region
    constellation: str | None = None
    affiliation: str
    description: str

class FilterOptions(BaseModel):
    regions: list[Region] = Field(default=None, description="Lista de regiões para filtrar")
    visions: list[Vision] = Field(default=None, description="Lista de visões para filtrar")
    weapon_types: list[WeaponType] = Field(default=None, description="Lista de armas para filtrar")
    rarities: list[int] = Field(default=None, description="Raridades existentes")
    combat_roles: list[str] = Field(default=None, description="Funções de combate")

class CharacterPage(BaseModel):
    """"Resposta paginada da listagem de personagens."""
    total: int = Field(description="Total de personagens após aplicar filtros.")
    limit: int = Field(description="Limite de personagens por página")
    offset: int = Field(description="Quantos itens foram pulados")
    characters: list[Character] = Field(description="Personagens da página atual.")