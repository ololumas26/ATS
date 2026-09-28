# schemas/cv_schema.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class ExperienciaProfissional(BaseModel):

    # Força o Pydantic a gerar "additionalProperties": False
    model_config = ConfigDict(extra="forbid")

    company: str = Field(description="Nome da empresa")
    role: str = Field(description="Cargo ocupado")
    start: str = Field(description="Data ou ano de início (ex: 'Jan 2021' ou '2021')")
    end: Optional[str] = Field(description="Data de fim ou 'Presente'/'Atual'")
    activity_description: List[str] = Field(description="Lista com as principais responsabilidades/conquistas")


class CurriculoEstruturado(BaseModel):

    # Força o Pydantic a gerar "additionalProperties": False
    model_config = ConfigDict(extra="forbid")

    candidate_name: str = Field(description="Nome completo do candidato")
    email: Optional[str] = Field(description="E-mail de contato")
    phone_number: Optional[str] = Field(description="Telefone/WhatsApp de contato")
    candidate_location: Optional[str] = Field(description="Localização do candidato (cidade e estado/país)")
    
    technical_skills: List[str] = Field(
        description="Lista de hard skills/ferramentas mencionadas (ex: Python, Docker, SQL)"
    )
    total_experience_years: float = Field(
        description="Estimativa total do tempo de experiência em anos com base no histórico profissional"
    )
    #experiences: List[ExperienciaProfissional] = Field(description="Lista de experiências profissionais ordenadas da mais recente para a mais antiga")
    profile_resume: str = Field(description="Um resumo executivo do perfil do candidato escrito pela IA em 2 a 3 frases")