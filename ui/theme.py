"""Cores usadas pela interface."""

# Cor de cada elemento (Vision), em hexadecimal. São aproximações das cores
# do jogo; ajuste à vontade.
VISION_COLORS = {
    "Pyro": "#EF7938",
    "Hydro": "#4CC2F1",
    "Anemo": "#74C2A8",
    "Electro": "#AF8EC1",
    "Dendro": "#A5C83B",
    "Cryo": "#9FD6E3",
    "Geo": "#FACB3E",
}

# Cor usada se aparecer um elemento que não está no dicionário acima
DEFAULT_COLOR = "#9E9E9E"


def vision_color(vision: str) -> str:
    """Devolve a cor do elemento, ou a cor padrão se ele for desconhecido."""
    return VISION_COLORS.get(vision, DEFAULT_COLOR)