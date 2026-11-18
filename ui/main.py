"""Interface visual da API Genshin Impact (NiceGUI)."""
from nicegui import ui

from api_client import ApiError, fetch_characters
from components import character_card


# response_timeout: tempo máximo (em segundos) para montar a página.
@ui.page("/", response_timeout=15)
async def index() -> None:
    """Página inicial: mostra a primeira página de personagens em cartões."""
    ui.label("API Genshin Impact").classes("text-h4")

    try:
        # await: espera a API sem travar a interface
        page = await fetch_characters(limit=12)
    except ApiError as exc:
        # text-negative é a cor de erro do Quasar (vermelho)
        ui.label(str(exc)).classes("text-negative")
        return

    ui.label(f"{page['total']} personagens (mostrando {len(page['characters'])})")

    # Grade que se adapta à largura: colunas de no mínimo 260px, que dividem o espaço
    with ui.grid(columns="repeat(auto-fill, minmax(260px, 1fr))").classes("w-full gap-4"):
        for character in page["characters"]:
            character_card(character)


ui.run(title="Genshin Impact")