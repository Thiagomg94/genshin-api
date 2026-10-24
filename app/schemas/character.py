""""Modelos Pydantic que definem o formato de um personagem"""
from pydantic import BaseModel, Field

class Character(BaseModel):
    """"Um personagem de Genshin Impact, no mesmo modelo do JSON"""
    id: str = Field(description="Identificar único, ex.: hu-tao")
    name: str
    title: str
    vision: str
    weapon_type: str
    rarity: int
    combat_role: str
    region: str
    constellation: str | None = None
    affiliation: str
    description: str