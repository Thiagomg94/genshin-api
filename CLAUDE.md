# CLAUDE.md - [API Genshin Impact]

## 📝 Descrição Geral

- **O que é:** Uma API que retorna ao usuário dados sobre personagens de Genshin Impact.
- **Público-alvo:** Qualquer pessoa que jogue Genshin Impact, sem restrições de idade.
- **Objetivo Atual:** Criar a estrutura necessária para que o usuário possa fazer requisições na API.

## 🛠️ Stack & Ambiente

- **Frontend/Backend:** FASTApi
- **Linguagem:** Python

## 🚀 Comandos Úteis

- Criar ambiente virtual: `python -m venv venv`
- Ativar ambiente (Windows): `venv\Scripts\activate`
- Ativar ambiente (Linux/Mac): `source venv/bin/activate`
- Instalar dependências: `pip install -r requirements.txt`
- Dev (servidor com reload): `uvicorn app.main:app --reload`
- Testes: `pytest`
- Docs interativas (Swagger): `http://localhost:8000/docs`
- Docs alternativas (ReDoc): `http://localhost:8000/redoc`

## 🎯 Regras de Código (Guia da IA)

- Escreva código limpo, modular e com tratamento de erros.
- Não adicione comentários óbvios, foque em código legível.
- Responda de forma direta, priorizando blocos de código completos.
- Os códigos gerados devem vir acompanhados de comentários explicando o que está sendo feito.
- Docstrings devem ser geradas quando necessárias.