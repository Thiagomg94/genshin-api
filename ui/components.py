"""Interface visual da API Genshin Impact (NiceGUI)."""
from nicegui import ui

from theme import vision_color


def character_card(character: dict) -> None:
    """Desenha o cartão de um personagem (um item de `items` da API)."""
    color = vision_color(character["vision"])

    # Faixa colorida no topo do cartão, na cor do elemento
    with ui.card().classes("w-full").style(f"border-top: 6px solid {color}"):
        ui.label(character["name"]).classes("text-h6")
        ui.label(character["title"]).classes("text-caption text-grey")

        # Estrelas: raridade de 4 ou 5 em um máximo de 5 (somente leitura)
        ui.rating(max=5, value=character["rarity"]).props("readonly size=sm color=amber")

        # Etiqueta com o elemento, na cor correspondente
        ui.badge(character["vision"], color=color)

        ui.label(f"{character['weapon_type']} · {character['region']}")
        ui.label(character["combat_role"]).classes("text-caption")