"""Configurações dos gráficos usados na página de estatísticas."""
from theme import vision_color, rarity_color


TEXT_COLOR = "gray"


def _title(text: str) -> dict:
    """Bloco de título padrão dos gráficos."""
    return {"text": text, "textStyle": {"color": TEXT_COLOR, "fontSize": 14}}


def bar_options(title: str, items: list[dict]) -> dict:
    """Gráfico de barras horizontais.
    
    Duas listas paralelas com os dados: uma com nomes e outra com números.
    """
    return {
        "title": _title(title),
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        # Margem esquerda maior para caber nomes maiores
        "grid": {"left": 90, "right": 32, "top": 40, "bottom": 16},
        "xAxis": {"type": "value", "axisLabel": {"color": TEXT_COLOR}},
        "yAxis": {
            "type": "category",
            "data": [item["label"] for item in items],
            "inverse": True,
            "axisLabel": {"color": TEXT_COLOR},
        },
        "series": [
            {
                "type": "bar",
                "data": [item["count"] for item in items],
                # Mostra o número no fim de cada barra.
                "label": {"show": True, "position": "right", "color": TEXT_COLOR},
            }

        ],
    }


def donut_options(title: str, items: list[dict], color_of=None) -> dict:
    """Gráfico de rosca.
    
    Para os dados no gráfico de pizza é preciso uma lista de fatias.
    Cada fatia é um dicionário.
    """

    data = []
    for item in items:
        slice_ = {"name": item["label"], "value": item["count"]}
        if color_of:
            # itemStyle.color define a cor de uma fatia específica.
            slice_["itemStyle"] = {"color": color_of(item["label"])}
        data.append(slice_)

    return {
        "title": _title(title),
        "tooltip": {"trigger": "item"},
        "legend": {"bottom": 0, "textStyle": {"color": TEXT_COLOR}},
        "series": [
            {
                "type": "pie",
                "radius": ["40%", "68%"],
                "center": ["50%", "50%"],
                "label": {"color": TEXT_COLOR, "formatter": "{b}: {c}"},
                "data": data,
            }
        ],
    }