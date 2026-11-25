# CLAUDE.md - [API Genshin Impact]

## 📝 Descrição Geral

- **O que é:** Uma API que retorna ao usuário dados sobre personagens de Genshin Impact.
- **Público-alvo:** Qualquer pessoa que jogue Genshin Impact, sem restrições de idade.
- **Objetivo Atual:** Polimento da API e migração do JSON para SQLite.

## 🛠️ Stack & Ambiente

- **Backend:** FastAPI
- **Linguagem:** Python 3.11+
- **Bibliotecas:** Pydantic, pydantic-settings, Uvicorn
- **Testes:** pytest e httpx2
- **Dados:** `app/data/characters.json` (117 personagens), somente leitura
- **Interface:** NiceGUI 4 (`ui/`), consome a API via `httpx2`

## 🏗️ Arquitetura

Fluxo da requisição: `endpoint → service → repository → dados`. Cada camada só importa da camada de baixo.

- `app/api/v1/endpoints/`: rotas HTTP (só recebem parâmetros e devolvem respostas)
- `app/api/deps.py`: injeção de dependências (`get_repository`, `get_character_service`)
- `app/services/`: regras de negócio (paginação, levanta `CharacterNotFoundError`)
- `app/repositories/`: acesso aos dados e filtros (hoje JSON; no futuro, banco)
- `app/schemas/`: modelos Pydantic e Enums (`Region`, `Vision`, `WeaponType`)
- `app/core/`: configurações (`config.py`) e erros globais (`exceptions.py`)
- Rotas da v1 ficam sob `/api/v1`
- `ui/`: interface NiceGUI, separada da API. Só conversa com ela por HTTP e nunca importa de `app/`
  - `api_client.py`: chamadas assíncronas à API (`fetch_characters`, `fetch_filter_options`)
  - `components.py`: componentes visuais (`character_card`, `character_detail`)
  - `theme.py`: cores por elemento
  - `main.py`: página, estado (`SearchState`) e eventos
  - `charts.py`: configurações dos gráficos

Convenções:
- O serviço não usa `HTTPException`: levanta exceções do domínio, e o handler global converte em HTTP.
- Filtros de texto são parciais e ignoram maiúsculas e acentos (`_normalize` no repositório).
- Só o dono do projeto cadastra personagens, editando o JSON (sem endpoints de escrita).
- Na interface, o estado da página fica em um `SearchState` (um por cliente) e a tela é redesenhada com `@ui.refreshable`.
- Respostas antigas da API são descartadas com `request_id`.
- Toda chamada à API na interface é `async` e trata `ApiError`.

## 🚀 Comandos Úteis

- Criar ambiente virtual: `python -m venv .venv`
- Ativar ambiente (Windows): `.venv\Scripts\activate`
- Ativar ambiente (Linux/Mac): `source .venv/bin/activate`
- Instalar dependências: `pip install -r requirements.txt`
- Dev (servidor com reload): `uvicorn app.main:app --reload`
- Testes: `pytest -v`
- Docs interativas (Swagger): `http://localhost:8000/docs`
- Docs alternativas (ReDoc): `http://localhost:8000/redoc`
- Instalar dependências da interface: `pip install -r ui/requirements.txt`
- Rodar a interface (com a API no ar): `python ui/main.py` → `http://localhost:8080`
- Variável `API_BASE_URL` muda o endereço da API usado pela interface

## 🎯 Regras de Código (Guia da IA)

- Escreva código limpo, modular e com tratamento de erros.
- Não adicione comentários óbvios, foque em código legível.
- Responda de forma direta, priorizando blocos de código completos.
- Os códigos gerados devem vir acompanhados de comentários explicando o que está sendo feito.
- Docstrings devem ser geradas quando necessárias.
- Commits no padrão Conventional Commits (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`), um assunto por commit, descrição em português no imperativo.
- Todo código novo de rota ou regra deve vir acompanhado de testes em `tests/`.