# schemas/job_schema.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class VagaEstruturada(BaseModel):

    # Força o Pydantic a gerar "additionalProperties": False
    model_config = ConfigDict(extra="forbid")

    job_title: str = Field(description="Título da vaga (ex: 'Backend Developer')")
    company_name: Optional[str] = Field(description="Nome da empresa que publica a vaga")
    job_location: Optional[str] = Field(description="Localização da vaga (cidade e estado/país) ou 'Remoto'")

    required_skills: List[str] = Field(
        description="Lista de hard skills/ferramentas exigidas (ex: Python, Docker, SQL)"
    )
    min_experience_years: float = Field(
        description="Anos mínimos de experiência exigidos para a vaga"
    )
    job_description: str = Field(description="Descrição da vaga e do perfil procurado")
