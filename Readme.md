# ATS — Applicant Tracking System

API que avalia o quão compatível um candidato é com uma vaga. Recebe o currículo em PDF e a descrição da vaga em texto, e devolve o currículo estruturado, um score de compatibilidade e uma explicação desse score escrita para o candidato.

## Como funciona

```
CV (PDF) ──► pypdf ──► OpenAI (JSON estruturado) ──► texto para embedding ──► embedding ─┐
                                                                                         ├─► similaridade do cosseno ──► score
Descrição da vaga (texto) ─────────────────────────────────────────────────► embedding ─┘
                                                                                                        │
CV estruturado + descrição da vaga ──► OpenAI (JSON estruturado) ──► explicação ◄───────────────────────┘
```

1. **Validação e extração:** o PDF é validado (tipo, extensão, não vazio), gravado num ficheiro temporário e o texto é extraído com `pypdf`. O ficheiro temporário é apagado logo após a extração.
2. **Estruturação:** o texto é enviado ao `gpt-4o-mini` com um JSON Schema estrito gerado a partir do modelo Pydantic `CurriculoEstruturado`, por isso a resposta vem sempre no mesmo formato.
3. **Embeddings:** o CV estruturado é convertido num texto curto (localização, experiência, perfil e skills) e, tal como a descrição da vaga, transformado num vetor de 1536 dimensões com `text-embedding-3-small`.
4. **Score:** a similaridade do cosseno entre os dois vetores, calculada com uma implementação própria (`CosineSimilarity`).
5. **Explicação:** o CV estruturado e a vaga são enviados ao `gpt-4o-mini`, também com JSON Schema estrito, que devolve um resumo, skills em comum, skills em falta, pontos fortes e lacunas, em português europeu e dirigidos ao candidato.

## API

### `POST /analyze`

Pedido `multipart/form-data`:

| Campo | Tipo | Descrição |
|---|---|---|
| `cv_file` | ficheiro | Currículo em PDF |
| `job_description` | texto | Descrição da vaga (não pode estar vazia) |

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "cv_file=@curriculo.pdf;type=application/pdf" \
  -F "job_description=Procuramos um Backend Developer Python com FastAPI e PostgreSQL..."
```

Resposta (resumida):

```json
{
  "cv": {
    "candidate_name": "...",
    "candidate_location": "Luanda, Angola",
    "technical_skills": ["Python", "FastAPI", "PostgreSQL"],
    "total_experience_years": 3,
    "profile_resume": "..."
  },
  "score": 0.52,
  "explanation": {
    "summary": "...",
    "matched_skills": ["Python", "FastAPI"],
    "missing_skills": ["Docker"],
    "strengths": ["..."],
    "gaps": ["..."]
  }
}
```

Erros:

| Código | Quando |
|---|---|
| `400` | O ficheiro não é um PDF, não tem extensão `.pdf` ou está vazio |
| `422` | Falta o ficheiro ou a descrição da vaga, ou a descrição só tem espaços |

A documentação interativa fica disponível em `/docs` com o servidor a correr.

## Estrutura do projeto

```
ats/
├── app.py                                # aplicação FastAPI
├── routers/
│   └── analysis_router.py                # POST /analyze
├── services/
│   ├── analysis_orchestrator_service.py  # orquestra o fluxo completo da análise
│   ├── pdf_service.py                    # extração de texto do PDF
│   ├── cv_parser_service.py              # PDF -> CV estruturado
│   ├── openai_service.py                 # cliente OpenAI: estruturação do CV e explicação do score
│   ├── vector_store_service.py           # texto para embedding + geração de embeddings
│   ├── calc_cossin_service.py            # similaridade do cosseno
│   └── qdrant_service.py                 # cliente Qdrant (ver "Estado atual")
├── schemas/
│   ├── analysis_schema.py                # AnalyzeForm (formulário do /analyze)
│   ├── cv_schema.py                      # CurriculoEstruturado
│   ├── job_schema.py                     # VagaEstruturada
│   └── score_explanation_schema.py       # ExplicacaoScore
├── config/settings.py                    # carrega o .env
├── utils/json_utils.py
└── exceptions/app_exceptions.py
```

## Como correr

Requisitos: Python 3.10+ e uma chave da API da OpenAI.

```bash
git clone https://github.com/ololumas26/ATS.git
cd ATS

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # e coloca a tua OPENAI_API_KEY

uvicorn app:app --reload
```

A API fica em `http://127.0.0.1:8000` e a documentação em `http://127.0.0.1:8000/docs`.

## Estado atual e limitações

- **O score é o cosseno bruto.** Serve para ordenar candidatos, mas não é uma percentagem de compatibilidade: com `text-embedding-3-small` os valores tendem a ficar numa faixa estreita. Uma versão futura deveria calibrá-lo com dados reais.
- **O texto do CV e o da vaga têm formatos diferentes.** O CV entra no embedding como texto estruturado com etiquetas e a vaga como texto livre, o que tende a baixar o score em geral.
- **Cada análise faz 4 chamadas à OpenAI:** estruturação do CV, dois embeddings e a explicação.
- **O Qdrant não é usado pela API.** O `qdrant_service.py` e os modelos `VagaEstruturada`/`structured_job_to_string` vêm de uma fase anterior em que os candidatos eram guardados numa base vetorial para pesquisa.
- **Dados pessoais:** o texto do CV é enviado à OpenAI e fica sujeito às políticas de retenção da API. A aplicação em si não guarda os currículos.
