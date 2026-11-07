"""Exceções do domínio e handlers globais de erro."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class CharacterNotFoundError(Exception):
    """Exceção para quando um personagem não é encontrado."""

    def __init__(self, character_id: str) -> None:
        self.character_id = character_id
        self.message = f"Personagem com ID {character_id} não encontrado."
        super().__init__(self.message)


async def character_not_found_handler(
    request: Request, exc: CharacterNotFoundError
) -> JSONResponse:
    """Converte CharacterNotFoundError em uma resposta HTTP 404."""
    return JSONResponse(status_code=404, content={"detail": exc.message})


def register_exception_handlers(app: FastAPI) -> None:
    """Registra os handlers de erro no aplicativo FastAPI."""
    app.add_exception_handler(CharacterNotFoundError, character_not_found_handler)