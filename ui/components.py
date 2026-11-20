"""Interface visual da API Genshin Impact (NiceGUI)."""
from collections.abc import Callable

from nicegui import ui

from theme import vision_color

# Texto escuro nas etiquetas
BADGE_TEXT_COLOR = "black"

def _rarity_stars(rarity: int) -> None:
    """Estrelas somente leitura: raridade de 4 ou 5."""
    ui.rating(max=5, value=rarity).props("readonly size=sm color=amber")


def _vision_badge(vision: str) -> None:
    """Etiqueta com o nome do elemento, na cor correspondente."""
    ui.badge(vision, color=vision_color(vision), text_color=BADGE_TEXT_COLOR)


def _info(label: str, value: str) -> None:
    """Uma linha 'rótulo: valor' da janela de detalhe."""
    with ui.row().classes("gap-1"):
        ui.label(f"{label}:").classes("text-bold")
        ui.label(value)


def character_card(
    character: dict, on_click: Callable[[dict], None] | None = None
) -> None:
    """Desenha o cartão de um personagem (um item de `items` da API).
    
    Se 'on_click' for informado, o cartão fica clicável e chama essa função
    com os dados do personagem."""
    color = vision_color(character["vision"])

    # Faixa colorida no topo do cartão, na cor do elemento
    card = ui.card().classes("w-full").style(f"border-top: 6px solid {color}")
    if on_click is not None:
        # Mão e sombra ao passar o mouse indicam que o cartão é clicável
        card.classes("cursor-pointer hover:shadow-lg")
        # character=character fixa o personagem deste cartão dentro da lambda
        card.on("click", lambda character=character: on_click(character))

    with card:
        ui.label(character["name"]).classes("text-h6")
        ui.label(character["title"]).classes("text-caption text-grey")
        _rarity_stars(character["rarity"])
        _vision_badge(character["vision"])
        ui.label(f"{character["weapon_type"]} · {character['region']}")
        ui.label(character["combat_role"]).classes("text-caption")


def character_detail(character: dict, on_close: Callable[[], None]) -> None:
    """Desenha o conteúdo da janela de detalhe de um personagem."""
    color = vision_color(character["vision"])

    ui.label(character["name"]).classes("text-h5").style(
        f"border-bottom: 4px solid {color}"
    )
    ui.label(character["title"]).classes("text-caption text-grey")
    _rarity_stars(character["rarity"])
    _vision_badge(character["vision"])

    _info("Arma", character["weapon_type"])
    _info("Região", character["region"])
    _info("Função", character["combat_role"])
    # Alguns personagens não tem constelação cadastrada
    _info("Constelação", character["constellation"] or "-")
    _info("Afiliação", character["affiliation"])

    ui.label(character["description"]).classes("text-body2")
    ui.button("Fechar", on_click=on_close).props("flat")