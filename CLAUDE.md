# CLAUDE.md - [API Genshin Impact]

## 📝 Descrição Geral

- **O que é:** Uma API que retorna ao usuário dados sobre personagens de Genshin Impact.
- **Público-alvo:** Qualquer pessoa que jogue Genshin Impact, sem restrições de idade.
- **Objetivo Atual:** Evoluir a API já funcional (listagem com filtros e busca por id): rota de valores disponíveis para os filtros, resposta paginada com total e, depois, migração do JSON para SQLite.

## 🛠️ Stack & Ambiente

- **Backend:** FastAPI
- **Linguagem:** Python 3.11+
- **Bibliotecas:** Pydantic, pydantic-settings, Uvicorn
- **Testes:** pytest e httpx2
- **Dados:** `app/data/characters.json` (117 personagens), somente leitura

## 🏗️ Arquitetura

Fluxo da requisição: `endpoint → service → repository → dados`. Cada camada só importa da camada de baixo.

- `app/api/v1/endpoints/`: rotas HTTP (só recebem parâmetros e devolvem respostas)
- `app/api/deps.py`: injeção de dependências (`get_repository`, `get_character_service`)
- `app/services/`: regras de negócio (paginação, levanta `CharacterNotFoundError`)
- `app/repositories/`: acesso aos dados e filtros (hoje JSON; no futuro, banco)
- `app/schemas/`: modelos Pydantic e Enums (`Region`, `Vision`, `WeaponType`)
- `app/core/`: configurações (`config.py`) e erros globais (`exceptions.py`)
- Rotas da v1 ficam sob `/api/v1`

Convenções:
- O serviço não usa `HTTPException`: levanta exceções do domínio, e o handler global converte em HTTP.
- Filtros de texto são parciais e ignoram maiúsculas e acentos (`_normalize` no repositório).
- Só o dono do projeto cadastra personagens, editando o JSON (sem endpoints de escrita).

## 🚀 Comandos Úteis

- Criar ambiente virtual: `python -m venv .venv`
- Ativar ambiente (Windows): `.venv\Scripts\activate`
- Ativar ambiente (Linux/Mac): `source .venv/bin/activate`
- Instalar dependências: `pip install -r requirements.txt`
- Dev (servidor com reload): `uvicorn app.main:app --reload`
- Testes: `pytest -v`
- Docs interativas (Swagger): `http://localhost:8000/docs`
- Docs alternativas (ReDoc): `http://localhost:8000/redoc`

## 🎯 Regras de Código (Guia da IA)

- Escreva código limpo, modular e com tratamento de erros.
- Não adicione comentários óbvios, foque em código legível.
- Responda de forma direta, priorizando blocos de código completos.
- Os códigos gerados devem vir acompanhados de comentários explicando o que está sendo feito.
- Docstrings devem ser geradas quando necessárias.
- Commits no padrão Conventional Commits (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`), um assunto por commit, descrição em português no imperativo.
- Todo código novo de rota ou regra deve vir acompanhado de testes em `tests/`.