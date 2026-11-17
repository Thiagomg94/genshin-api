"""Testes para os endpoints de personagens."""

from app.schemas.character import Region, Vision, WeaponType

def test_root(client):
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_all(client):
    """Testa o endpoint de listagem de personagens."""
    response = client.get("/api/v1/characters")
    assert response.status_code == 200
    assert len(response.json()["characters"]) == 5

def test_filter_by_region(client):
    response = client.get("/api/v1/characters", params={"region": "Inazuma"})
    ids = {c["id"] for c in response.json()["characters"]}
    assert ids == {"ayaka", "thoma"}

def test_filter_ignores_case(client):
    response = client.get("/api/v1/characters", params={"region": "inazuma"})
    assert len(response.json()["characters"]) == 2

def test_combined_filters(client):
    response = client.get("/api/v1/characters", params={"region": "Inazuma", "vision": "cryo"})
    assert [c["id"] for c in response.json()["characters"]] == ["ayaka"]

def test_filter_by_rarity(client):
    response = client.get("/api/v1/characters", params={"rarity": 5})
    assert len(response.json()["characters"]) == 3

def test_without_results(client):
    response = client.get("/api/v1/characters", params={"region": "Natlan"})
    assert response.status_code == 200
    assert response.json()["characters"] == []

def test_pagination(client):
    response = client.get("/api/v1/characters", params={"limit": 2, "offset": 4})
    assert len(response.json()["characters"]) == 1 # Pula 4 e sobra 1

def test_get_by_id(client):
    response = client.get("/api/v1/characters/diluc")
    assert response.status_code == 200
    assert response.json()["name"] == "Diluc"

def test_get_by_id_not_found(client):
    response = client.get("/api/v1/characters/abc")
    assert response.status_code == 404
    assert "abc" in response.json()["detail"]

def test_invalid_rarity(client):
    response = client.get("/api/v1/characters", params={"rarity": 6})
    assert response.status_code == 422

def test_invalid_region_returns_422(client):
    response = client.get("/api/v1/characters", params={"region": "Atlantis"})
    assert response.status_code == 422

def test_by_combat_role_partial(client):
    response = client.get("/api/v1/characters", params={"combat_role": "healer"})
    assert [c["id"] for c in response.json()["characters"]] == ["barbara"]

def test_filter_by_affiliation_ignores_accents(client):
    # "cla" sem acento deve encontrar "Clã Kamisato"
    response = client.get("/api/v1/characters", params={"affiliation": "cla"})
    assert {c["id"] for c in response.json()["characters"]} == {"ayaka", "thoma"}

def test_search_by_name(client):
    response = client.get("/api/v1/characters", params={"q": "HU TAO"})
    assert [c["id"] for c in response.json()["characters"]] == ["hu-tao"]

def test_combined_text_and_enum_filters(client):
    response = client.get("/api/v1/characters", params={"combat_role": "main dps", "region": "Inazuma"})
    assert [c["id"] for c in response.json()["characters"]] == ["ayaka"]

def test_filters_route_returns_available_values(client):
    response = client.get("/api/v1/characters/filters")
    assert response.status_code == 200

    body = response.json()
    # Enums seguem a ordem declarada no schema, e só entram valores presentes
    assert body["regions"] == [r.value for r in Region if r.value in {"Mondstadt", "Liyue", "Inazuma"}]
    assert body["visions"] == [v.value for v in Vision if v.value in {"Cryo", "Hydro", "Pyro"}]
    assert body["weapon_types"] == [wt.value for wt in WeaponType if wt.value in {"Sword", "Claymore", "Polearm", "Catalyst"}]
    assert body["rarities"] == [4, 5]

def test_filters_route_returns_combat_roles_split(client):
    response = client.get("/api/v1/characters/filters")
    roles = response.json()["combat_roles"]

    # "Healer/Support" deve virar duas funções separadas
    assert roles == ["Healer", "Main DPS", "Support"]
    assert "Healer/Support" not in roles   
    
def test_list_returns_pagination_info(client):
    body = client.get("/api/v1/characters", params={"limit": 2, "offset": 1}).json()
    assert body["total"] == 5
    assert body["limit"] == 2
    assert body["offset"] == 1
    assert len(body["characters"]) == 2

def test_total_counts_all_filtered_results_not_just_the_page(client):
    body = client.get(
        "/api/v1/characters", params={"region": "Inazuma", "limit": 1}
    ).json()
    assert body["total"] == 2 # os dois de Inazuma, mesmo com limit=1
    assert len(body["characters"]) == 1

def test_offset_beyond_total_returns_empty_items(client):
    body = client.get("/api/v1/characters", params={"offset": 100}).json()
    assert body["total"] == 5
    assert body["characters"] == []