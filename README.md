# API Genshin Impact

API REST construída com **Python** e **FastAPI** que retorna informações sobre personagens do jogo *Genshin Impact*, com busca por filtros (por exemplo, listar os personagens de Inazuma).

> 🚧 **Projeto em desenvolvimento.** Veja o [status](#status-do-projeto) para saber o que já funciona e o que falta.

## Tecnologias

- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/) (validação dos dados)
- Uvicorn (servidor)
- Pytest + HTTPX (testes)

## Status do projeto

**Concluído**
- [x] Estrutura de pastas em camadas
- [x] Schema do personagem (`app/schemas/character.py`)
- [x] Base de dados inicial em JSON, com 117 personagens (`app/data/characters.json`)
- [x] Repositório com leitura do JSON e filtros (`app/repositories/character_repository.py`)
- [x] Endpoints de personagens: listagem com filtros e paginação, e busca por id (`app/api/v1/endpoints/characters.py`)

**Em andamento / próximos passos**
- [x] Registrar o router da v1 no `main.py` (`app/api/v1/router.py`)
- [ ] Camada de serviço com as regras de negócio (`app/services/`)
- [ ] Configurações centralizadas com variáveis de ambiente (`app/core/config.py`)
- [ ] Tratamento global de erros (`app/core/exceptions.py`)
- [ ] Testes automatizados com pytest
- [ ] Usar `Enum` para região, elemento e arma, com validação e lista suspensa no Swagger
- [ ] Mais filtros: função em combate, afiliação e busca por nome
- [ ] Futuro: migrar de JSON para SQLite + SQLAlchemy

## Estrutura do projeto

```
genshin-api/
├── app/
│   ├── main.py                    # Cria o FastAPI e registra os routers
│   ├── core/                      # Configurações e exceções globais
│   ├── api/
│   │   ├── deps.py                # Dependências injetáveis
│   │   └── v1/
│   │       ├── router.py          # Agrega os routers da v1
│   │       └── endpoints/
│   │           └── characters.py  # Rotas de personagens
│   ├── schemas/
│   │   └── character.py           # Modelos Pydantic
│   ├── services/
│   │   └── character_service.py   # Regras de negócio
│   ├── repositories/
│   │   └── character_repository.py  # Acesso aos dados (JSON hoje, banco no futuro)
│   └── data/
│       └── characters.json        # Dados dos personagens
├── tests/                         # Testes automatizados (pytest)
├── .env.example                   # Modelo de variáveis de ambiente
├── requirements.txt
├── CLAUDE.md
└── README.md
```

A requisição passa pelas camadas nesta ordem: **endpoint → serviço → repositório → dados**. Cada camada tem uma responsabilidade, então trocar o JSON por um banco no futuro exige mudar apenas o repositório.

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Thiagomg94/genshin-api.git
cd genshin-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

## Como executar

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Documentação interativa (Swagger): http://localhost:8000/docs

### Filtros de `/characters`

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `region` | texto | Região (ex.: `Inazuma`) |
| `vision` | texto | Elemento (ex.: `Cryo`) |
| `weapon_type` | texto | Tipo de arma (ex.: `Polearm`) |
| `rarity` | 4 ou 5 | Raridade em estrelas |
| `limit` | inteiro | Itens por página (padrão 20, máximo 100) |
| `offset` | inteiro | Quantos itens pular (padrão 0) |

Os filtros são opcionais e podem ser combinados.

### Exemplos de requisição

```bash
# Todos os personagens de Inazuma
curl "http://localhost:8000/characters?region=Inazuma"

# Personagens Cryo de 5 estrelas
curl "http://localhost:8000/characters?vision=Cryo&rarity=5"

# Um personagem específico
curl "http://localhost:8000/characters/hu-tao"
```

### Exemplo de resposta

```json
{
  "id": "hu-tao",
  "name": "Hu Tao",
  "title": "Fragrance in Thaw",
  "vision": "Pyro",
  "weapon_type": "Polearm",
  "rarity": 5,
  "combat_role": "Main DPS",
  "region": "Liyue",
  "constellation": "Papilio Charontis",
  "affiliation": "Casa Funerária Wangsheng",
  "description": "77ª diretora da Casa Funerária Wangsheng, responsável pelos ritos funerários de Liyue."
}
```

## Testes

```bash
pytest
```

## Cadastro de personagens

Por enquanto a API é somente leitura. Novos personagens são adicionados editando `app/data/characters.json`, seguindo o formato de um personagem existente. O `id` deve ser único.

## Licença

Defina a licença do projeto (ex.: MIT).