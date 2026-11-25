"""Interface visual da API Genshin Impact (NiceGUI)."""
import math
from dataclasses import dataclass

from nicegui import ui

from api_client import ApiError, fetch_characters, fetch_filter_options, fetch_stats
from components import character_card, character_detail
from theme import vision_color, rarity_color
from charts import bar_options, donut_options

# Quantos cartões aparecem por página
PAGE_SIZE = 12


@dataclass
class SearchState:
    """Estado da busca: filtros escolhidos, página atual e último resultado."""

    q: str | None = None
    region: str | None = None
    vision: str | None = None
    weapon_type: str | None = None
    rarity: int | None = None
    page: int = 1
    data: dict | None = None # última resposta da API
    error: str | None = None # mensagem de erro, se a busca falhou
    request_id: int = 0 # numera as buscas, para descastar respostas antigas
    selected: dict | None = None # personagem aberto na janela de detalhe


# response_timeout: tempo máximo (em segundos) para montar a página
@ui.page("/", response_timeout=15)
async def index() -> None:
    """Página inicial: filtros, cartões de personagens e paginação."""
    dark = ui.dark_mode()

    # Cabeçalho
    with ui.row().classes("w-full items-center justify-between"):
        ui.label("API Genshin Impact").classes("text-h4")
        ui.link("📊 Estatísticas", "/estatisticas")
        ui.switch(
            "Tema escuro",
            on_change=lambda e: dark.enable() if e.value else dark.disable(),
        )

    try:
        # Os valores das listas suspensas vêm da rota /characters/filters
        options = await fetch_filter_options()
    except ApiError as exc:
        ui.label(str(exc)).classes("text-negative")
        return


    # Criado dentro da página: cada aba do navegador tem o seu próprio estado
    state = SearchState()

    async def load() -> None:
        """Busca a página atual na API e redesenha os resultados."""
        state.request_id += 1
        request_id = state.request_id
        offset = (state.page - 1) * PAGE_SIZE
        try:
            data = await fetch_characters(
                q=state.q,
                region = state.region,
                vision=state.vision,
                weapon_type=state.weapon_type,
                rarity=state.rarity,
                limit=PAGE_SIZE,
                offset=offset,
            )
            error = None
        except ApiError as exc:
            data, error = None, str(exc)

        # Se o usuário já pediu outra busca enquanto esta esperava, descarta esta
        if request_id != state.request_id:
            return
        state.data, state.error = data, error
        results.refresh()

    async def change_filter(name: str, value) -> None:
        """Atualiza um filtro, volta para a página 1 e busca novamente."""
        # Campo limpo ('' ou None) significa 'sem filtro'
        setattr(state, name, value or None)
        state.page = 1
        await load()

    async def change_page(page: int) -> None:
        """Vai para outra página dos resultados."""
        if page == state.page:  # evita buscar de novo sem necessidade
            return
        state.page = page
        await load()

    @ui.refreshable
    def detail_view() -> None:
        """Conteúdo da janela de detalhe, a partir do personagem selecionado."""
        if state.selected is not None:
            character_detail(state.selected, on_close=detail_dialog.close)

    def show_detail(character: dict) -> None:
        """Guarda o personagem clicado, redesenha a janela e a abre."""
        state.selected = character
        detail_view.refresh()
        detail_dialog.open()

    # Janela única, reaproveitada a cada clique em um cartão
    with ui.dialog() as detail_dialog:
        with ui.card().classes("w-96"):
            detail_view()

    @ui.refreshable
    def results() -> None:
        """Desenha cartões e paginação a partir do estado (não busca nada)."""
        if state.error:
            ui.label(state.error).classes("text-negative")
            return
        if state.data is None:
            ui.label("Carregando...")
            return

        total = state.data["total"]
        ui.label(f"{total} personagens encontrados")
        if total == 0:
            ui.label("Nenhum personagem com esses filtros.").classes("text-grey")
            return

        with ui.grid(columns="repeat(auto-fill, minmax(260px, 1fr))").classes("w-full gap-4"):
            for character in state.data["characters"]:
                character_card(character, on_click=show_detail)

        # Número de páginas = total / tamanho da página, arredondado para cima
        pages = math.ceil(total / PAGE_SIZE)
        if pages > 1:
            ui.pagination(
                1,
                pages,
                value=state.page,
                direction_links=True,
                on_change=lambda e: change_page(e.value),
            )

    # --- Filtros ---
    with ui.row().classes("w-full items-end gap-4"):
        ui.input(
            "Buscar por nome ou título",
            on_change=lambda e: change_filter("q", e.value),
        ).props("clearable debounce=500").classes("w-64")

        ui.select(
            options["regions"], label="Região", clearable=True,
            on_change=lambda e: change_filter("region", e.value),
        ).classes("w-48")

        ui.select(
            options["visions"], label="Elemento", clearable=True,
            on_change=lambda e: change_filter("vision", e.value),
        ).classes("w-48")

        ui.select(
            options["weapon_types"], label="Arma", clearable=True,
            on_change=lambda e: change_filter("weapon_type", e.value),
        ).classes("w-48")

        # Dicionário {valor: rótulo}: o valor enviado à API é o número (4 ou 5)
        ui.select(
            {rarity: f"{rarity} estrelas" for rarity in options["rarities"]},
            label="Raridade", clearable=True,
            on_change=lambda e: change_filter("rarity", e.value),
        ).classes("w-48")

    results()    # desenha o estado inicial ("Carregando...")
    await load()  # busca a primeira página e redesenha


@ui.page("/estatisticas", response_timeout=15)
async def stats_page():
    """Página com gráficos sobre a composição do catálogo de personagens."""
    with ui.row().classes("w-full items-center justify-between"):
        ui.label("Estatísticas").classes("text-2xl font-bold")
        # Link de volta para a página principal.
        ui.link("← Voltar aos personagens", "/")

    # Busca os dados; se a API estiver fora do ar, mostra o erro e para por aqui.
    try:
        stats = await fetch_stats()
    except ApiError as error:
        ui.label(f"Não foi possível carregar as estatísticas: {error}").classes("text-negative")
        return

    ui.label(f"{stats['total']} personagens no catálogo").classes("text-gray-500")

    # Grade que ajusta o número de colunas ao tamanho da tela.
    with ui.grid(columns="repeat(auto-fit, minmax(380px, 1fr))").classes("w-full gap-4"):
        charts = [
            bar_options("Personagens por região", stats["by_region"]),
            donut_options("Personagens por elemento", stats["by_vision"], color_of=vision_color),
            bar_options("Personagens por arma", stats["by_weapon_type"]),
            donut_options("Personagens por raridade (estrelas)", stats["by_rarity"], color_of=rarity_color),
        ]
        for options in charts:
            with ui.card():
                ui.echart(options).classes("w-full h-72")


ui.run(title="Genshin Impact")