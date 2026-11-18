"""Cliente HTTP da API Genshin Impact"""

import os

import httpx2 as httpx

# Endereço da API; pode ser trocado pela variável de ambiente API_BASE_URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
TIMEOUT_SECONDS = 10.0

class ApiError(Exception):
    """Falha ao obter dados da API (fora do ar, erro http, tempo esgotado.)"""


async def _get(path: str, params: dict | None = None) -> dict:
    """Faz um GET na API e devolve o JSON da resposta.
    
    Raises:
        ApiError: se a API não responder ou devolver um erro HTTP.
    """
    try:
        async with httpx.AsyncClient(
            base_url=API_BASE_URL, timeout=TIMEOUT_SECONDS
        ) as client:
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        # Cobre API fora do ar, timeout e respostas de erro
        raise ApiError(
            "Não foi possível obter os dados. Ela está rodando?"
        ) from exc


async def fetch_filter_options() -> dict:
    """Busca os valores disponíveis para os filtros (GET /characters/filters)."""
    return await _get("/characters/filters")


async def fetch_characters(
    *,
    region: str | None = None,
    vision: str | None = None,
    weapon_type: str | None = None,
    rarity: int | None = None,
    combat_role: str | None = None,
    affiliation: str | None = None,
    q: str | None = None,
    limit: int = 12,
    offset: int = 0,
) -> dict:
    """Busca uma página de personagens. (GET /characters.)
    
    Devolve o JSON paginado: {"total", "limit", "offset", "characters"}.
    """
    params = {
        "region": region,
        "vision": vision,
        "weapon_type": weapon_type,
        "rarity": rarity,
        "combat_role": combat_role,
        "affiliation": affiliation,
        "q": q,
        "limit": limit,
        "offset": offset,
    }
    # Filtros vazios não são enviados: "region=" resulta 422 por não ser valor válido.
    params = {key: value for key, value in params.items() if value not in (None, "")}
    return await _get("/characters", params=params)



if __name__ == "__main__":
    # Teste manual: python ui/api_client.py (com a API rodando)
    import asyncio

    async def demo() -> None:
        filters = await fetch_filter_options()
        print("Regiões:", filters["regions"])
        page = await fetch_characters(region="Inazuma", limit=2)
        print("Total em Inazuma:", page["total"])
        print("Primeiros:", [c["name"] for c in page["characters"]])

    asyncio.run(demo())