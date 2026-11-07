"""Testes para os endpoints de personagens."""

def test_root(client):
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_all(client):
    """Testa o endpoint de listagem de personagens."""
    response = client.get("/api/v1/characters")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_filter_by_region(client):
    response = client.get("/api/v1/characters", params={"region": "Inazuma"})
    ids = {c["id"] for c in response.json()}
    assert ids == {"ayaka", "thoma"}

def test_filter_ignores_case(client):
    response = client.get("/api/v1/characters", params={"region": "inazuma"})
    assert len(response.json()) == 2

def test_combined_filters(client):
    response = client.get("/api/v1/characters", params={"region": "Inazuma", "vision": "cryo"})
    assert [c["id"] for c in response.json()] == ["ayaka"]

def test_filter_by_rarity(client):
    response = client.get("/api/v1/characters", params={"rarity": 5})
    assert len(response.json()) == 3

def test_without_results(client):
    response = client.get("/api/v1/characters", params={"region": "Natlan"})
    assert response.status_code == 200
    assert response.json() == []

def test_pagination(client):
    response = client.get("/api/v1/characters", params={"limit": 2, "offset": 4})
    assert len(response.json()) == 1 # Pula 4 e sobra 1

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
    
