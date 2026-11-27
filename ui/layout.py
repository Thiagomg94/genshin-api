"""Layout compartilhado pelas páginas: tema, largura máxima e cabeçalho."""
from nicegui import app, ui

# Largura máxima do conteúdo
MAX_WIDTH = "1200px"


def setup_page() -> None:
    """Prepara a página atual. Primeira chamada de cada página."""
    # app.storage.user guarda dados no servidor por um cookie
    # setdefault define o tema claro só na primeira visita.
    app.storage.user.setdefault("dark_mode", False)

    # bind_value mantém o tema e valor guardados sempre iguais.
    dark = ui.dark_mode().bind_value(app.storage.user, "dark_mode")

    ui.query(".nicegui-content").classes("mx-auto w-full").style(
        f"max-width: {MAX_WIDTH}"
    )

    # Cabeçalho único
    with ui.row().classes("w-full items-center justify-between"):
        ui.label("API Genshin Impact").classes("text-h4")
        with ui.row().classes("items-center gap-4"):
            ui.link("Personagens", "/")
            ui.link("Estatísticas", "/estatisticas")
            ui.switch("Tema escuro").bind_value(dark)