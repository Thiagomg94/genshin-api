# API Genshin Impact

API REST construída com **Python** e **FastAPI** que retorna informações sobre personagens de *Genshin Impact*, com filtros por região, elemento, arma, raridade, função em combate, afiliação e busca por nome.

> Projeto de fãs, sem fins lucrativos e sem vínculo com a HoYoverse.
> Genshin Impact e todos os seus personagens e nomes pertencem à HoYoverse.

## Tecnologias

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/) e Uvicorn
- [Pydantic](https://docs.pydantic.dev/) e pydantic-settings (validação e configurações)
- Pytest e httpx2 (testes)

## Status do projeto

**Concluído**
- [x] Arquitetura em camadas (endpoint → serviço → repositório → dados)
- [x] Base de dados em JSON com 117 personagens
- [x] Endpoints de listagem (com filtros e paginação) e busca por id
- [x] `Enum` para região, elemento e arma, com validação e lista suspensa no Swagger
- [x] Filtros de texto parciais, que ignoram maiúsculas e acentos
- [x] Configurações centralizadas e leitura de variáveis de ambiente
- [x] Tratamento global de erros (404 padronizado)
- [x] Testes automatizados com pytest
- [x] Rota que lista os valores disponíveis para cada filtro

**Próximos passos**
- [ ] Resposta paginada com o total de resultados
- [ ] Migrar de JSON para SQLite + SQLAlchemy

## Estrutura do projeto

```
genshin-api/
├── app/
│   ├── main.py                       # Cria o FastAPI, registra routers e handlers de erro
│   ├── core/
│   │   ├── config.py                 # Configurações (pydantic-settings)
│   │   └── exceptions.py             # Exceções do domínio e handlers globais
│   ├── api/
│   │   ├── deps.py                   # Dependências injetáveis (repositório e serviço)
│   │   └── v1/
│   │       ├── router.py             # Agrega os routers da v1
│   │       └── endpoints/
│   │           └── characters.py     # Rotas de personagens
│   ├── schemas/
│   │   └── character.py             # Modelos Pydantic e Enums
│   ├── services/
│   │   └── character_service.py     # Regras de negócio (paginação, erros)
│   ├── repositories/
│   │   └── character_repository.py  # Acesso aos dados e filtros
│   └── data/
│       └── characters.json          # Dados dos personagens
├── tests/                            # Testes automatizados
├── .env.example                      # Modelo de variáveis de ambiente
├── requirements.txt
├── CLAUDE.md
└── README.md
```

Cada camada só conhece a de baixo. Trocar o JSON por um banco no futuro exige alterar apenas o repositório.

## Instalação

```bash
git clone https://github.com/Thiagomg94/genshin-api.git
cd genshin-api

python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/macOS

pip install -r requirements.txt
```

## Como executar

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger (documentação interativa): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Verifica se a API está no ar |
| GET | `/api/v1/characters` | Lista personagens, com filtros e paginação |
| GET | `/api/v1/characters/{id}` | Retorna um personagem pelo id (ex.: `hu-tao`) |
| GET | `/api/v1/characters/filters` | Lista os valores disponíveis para cada filtro |

### Filtros de `/api/v1/characters`

Todos são opcionais e podem ser combinados.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `region` | enum | `Mondstadt`, `Liyue`, `Inazuma`, `Sumeru`, `Fontaine`, `Natlan`, `Nod-Krai`, `Snezhnaya` |
| `vision` | enum | `Anemo`, `Cryo`, `Dendro`, `Electro`, `Geo`, `Hydro`, `Pyro` |
| `weapon_type` | enum | `Sword`, `Claymore`, `Polearm`, `Bow`, `Catalyst` |
| `rarity` | 4 ou 5 | Raridade em estrelas |
| `combat_role` | texto | Busca parcial na função em combate (ex.: `healer`) |
| `affiliation` | texto | Busca parcial na afiliação (ex.: `favonius`) |
| `q` | texto | Busca parcial no nome ou título (ex.: `raiden`) |
| `limit` | inteiro | Itens por página (padrão 10, máximo 100) |
| `offset` | inteiro | Quantos itens pular (padrão 0) |

Valores de enum e buscas de texto ignoram maiúsculas e minúsculas. As buscas de texto também ignoram acentos.

### Exemplos

```bash
# Personagens de Inazuma
curl "http://localhost:8000/api/v1/characters?region=Inazuma"

# Personagens Cryo de 5 estrelas
curl "http://localhost:8000/api/v1/characters?vision=Cryo&rarity=5"

# Curandeiros dos Cavaleiros de Favonius
curl "http://localhost:8000/api/v1/characters?combat_role=healer&affiliation=favonius"

# Busca por nome
curl "http://localhost:8000/api/v1/characters?q=raiden"

# Um personagem específico
curl "http://localhost:8000/api/v1/characters/hu-tao"
```

### Exemplo de resposta (`/characters/hu-tao`)

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

### Erros

| Código | Quando acontece |
|--------|-----------------|
| 404 | Personagem não encontrado: `{"detail": "Personagem 'xyz' não encontrado."}` |
| 422 | Parâmetro inválido (região inexistente, `rarity` fora de 4 e 5, etc.) |

## Configuração

Os valores padrão ficam em `app/core/config.py`. Para alterá-los, copie `.env.example` para `.env` e edite:

```
APP_NAME=API Genshin Impact
APP_VERSION=0.1.0
API_V1_PREFIX=/api/v1
```

## Testes

```bash
pytest -v
```

Os testes usam um repositório falso com poucos personagens, sem depender do `characters.json`.

## Cadastro de personagens

A API é somente leitura. Para adicionar um personagem, edite `app/data/characters.json` seguindo o formato de um existente. O `id` deve ser único, e `region`, `vision` e `weapon_type` precisam ser valores aceitos pelos enums em `app/schemas/character.py`.

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.