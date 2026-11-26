"""Fixtures compartilhadas pelos testes."""
import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_repository
from app.main import app
from app.repositories.character_repository import CharacterRepository
from app.schemas.character import Character
from app.core.rate_limit import limiter

def make_character(**overrides) -> Character:
    """Cria um personagem de teste."""
    data = {
        "id": "x",
        "name": "X",
        "title": "Título",
        "vision": "Pyro",
        "weapon_type": "Sword",
        "rarity": 4,
        "combat_role": "Support",
        "region": "Mondstadt",
        "constellation": None,
        "affiliation": "Teste",
        "description": "Descrição de teste",
    }
    data.update(overrides)
    return Character(**data)

@pytest.fixture
def client():
    """Cria um cliente de teste com repositório para a aplicação FastAPI."""
    limiter.enabled = False # demais testes não devem ser afetados pelo limite
    fake_repo = CharacterRepository(
        [
            make_character(id="diluc", name="Diluc", weapon_type="Claymore", rarity=5,
                           combat_role="Main DPS", affiliation="Adega Dawn"),
            make_character(id="barbara", name="Barbara", vision="Hydro",
                           weapon_type="Catalyst", combat_role="Healer/Support"),
            make_character(id="hu-tao", name="Hu Tao", weapon_type="Polearm",
                           rarity=5, region="Liyue", combat_role="Main DPS"),
            make_character(id="ayaka", name="Kamisato Ayaka", vision="Cryo",
                           rarity=5, region="Inazuma", combat_role="Main DPS", affiliation="Clã Kamisato"),
            make_character(id="thoma", name="Thoma", weapon_type="Polearm",
                           region="Inazuma", affiliation="Clã Kamisato"),
        ]
    )
    # Quando o endpoint pedir get_repository, o FastAPI entrega o falso
    app.dependency_overrides[get_repository] = lambda: fake_repo
    yield TestClient(app)
    # Troca após o teste para não afetar outros testes que usem get_repository
    app.dependency_overrides.clear()
