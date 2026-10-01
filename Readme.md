# ATS — Applicant Tracking System

Sistema de tracking de candidatos que visa encontrar o candidato ideal para uma determinada vaga.

O ATS lê currículos em PDF, usa a OpenAI para os transformar em dados estruturados, gera embeddings desses dados e guarda-os no [Qdrant](https://qdrant.tech/) para que possam ser comparados com vagas por semelhança semântica.

## Como funciona

```
CV (PDF) ──► extração de texto ──► OpenAI (JSON estruturado) ──► texto para embedding ──► embedding ──► Qdrant
                pypdf               gpt-4o-mini                                        text-embedding-3-small
```

1. **Extração** — o texto do PDF é lido com `pypdf`.
2. **Estruturação** — o texto é enviado à OpenAI (`gpt-4o-mini`) com um JSON Schema estrito gerado a partir do modelo Pydantic `CurriculoEstruturado`. A resposta volta sempre no mesmo formato.
3. **Texto para embedding** — os campos relevantes (localização, experiência, perfil e skills) são convertidos num texto curto e consistente.
4. **Embedding** — o texto é convertido num vetor de 1536 dimensões com `text-embedding-3-small`.
5. **Armazenamento** — o vetor é guardado no Qdrant (modo local, em disco), na coleção de candidatos.

As vagas seguem a mesma estrutura: o modelo `VagaEstruturada` é convertido num texto com **as mesmas etiquetas** do CV, para que os dois embeddings sejam comparáveis.

## Estrutura do projeto

```
ats/
├── main.py                        # ponto de entrada
├── config/
│   └── settings.py                # carrega o .env e expõe as configurações
├── schemas/
│   ├── cv_schema.py               # CurriculoEstruturado, ExperienciaProfissional
│   └── job_schema.py              # VagaEstruturada
├── services/
│   ├── pdf_service.py             # extração de texto de PDFs
│   ├── openai_service.py          # cliente OpenAI + extração estruturada do CV
│   ├── cv_parser_service.py       # orquestra PDF → OpenAI → dict
│   ├── vector_store_service.py    # texto para embedding (CV e vaga) + geração de embeddings
│   └── qdrant_service.py          # cliente Qdrant e criação da coleção
├── utils/
│   └── json_utils.py
└── exceptions/
    └── app_exceptions.py
```

## Requisitos

- Python 3.10+
- Uma chave da API da OpenAI

Dependências principais:

- `openai`
- `pydantic`
- `pypdf`
- `python-dotenv`
- `qdrant-client`

## Instalação

```bash
git clone <url-do-repositório>
cd ats

python3 -m venv venv
source venv/bin/activate

pip install openai pydantic pypdf python-dotenv qdrant-client
```

Cria um ficheiro `.env` na raiz do projeto:

```env
OPENAI_API_KEY=a-tua-chave
```

## Utilização

A partir da raiz do projeto:

```bash
python main.py
```

Isto lê o CV definido em `main.py`, estrutura-o, gera o embedding e grava-o no Qdrant.

> O Qdrant corre em modo local e guarda os dados em `./qdrant_files`. O caminho é relativo à pasta de onde o comando é executado, por isso corre sempre a partir da raiz do projeto.

### Converter uma vaga em texto

```python
from schemas.job_schema import VagaEstruturada
from services.vector_store_service import structured_job_to_string

vaga = VagaEstruturada(
    job_title='Backend Developer (Python)',
    company_name='Nzila Tech',
    job_location='Luanda, Angola (híbrido)',
    required_skills=['Python', 'FastAPI', 'PostgreSQL', 'Docker'],
    min_experience_years=2,
    job_description='Procuramos um Backend Developer para integrar a equipa de produto.',
).model_dump()

print(structured_job_to_string(vaga))
```

### Procurar os candidatos mais adequados a uma vaga

```python
from services.vector_store_service import gen_embedding_from_text
from services.qdrant_service import qclient, CV_COLLECTION_NAME

job_embedding = gen_embedding_from_text(structured_job_to_string(vaga))

resultados = qclient.query_points(
    collection_name=CV_COLLECTION_NAME,
    query=job_embedding,
    limit=10,
)
```

## Modelos de dados

### `CurriculoEstruturado`

| Campo | Tipo | Descrição |
|---|---|---|
| `candidate_name` | `str` | Nome completo do candidato |
| `email` | `str \| None` | E-mail de contacto |
| `phone_number` | `str \| None` | Telefone/WhatsApp |
| `candidate_location` | `str \| None` | Cidade e país |
| `technical_skills` | `list[str]` | Hard skills e ferramentas |
| `total_experience_years` | `float` | Anos de experiência estimados |
| `profile_resume` | `str` | Resumo do perfil em 2 a 3 frases |

### `VagaEstruturada`

| Campo | Tipo | Descrição |
|---|---|---|
| `job_title` | `str` | Título da vaga |
| `company_name` | `str \| None` | Empresa que publica a vaga |
| `job_location` | `str \| None` | Cidade e país, ou "Remoto" |
| `required_skills` | `list[str]` | Hard skills exigidas |
| `min_experience_years` | `float` | Anos mínimos de experiência |
| `job_description` | `str` | Descrição da vaga e do perfil procurado |

## Estado atual

- `main.py` processa um único CV, com o nome do ficheiro e o id do ponto definidos no código.
- A conversão de vagas em texto já existe, mas as vagas ainda não são guardadas no Qdrant.
- O score devolvido pelo Qdrant é o score bruto do cosseno: serve para ordenar candidatos, mas não é uma percentagem de compatibilidade.