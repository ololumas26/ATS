# schemas/score_explanation_schema.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List


class ExplicacaoScore(BaseModel):

    # Força o Pydantic a gerar "additionalProperties": False
    model_config = ConfigDict(extra="forbid")

    summary: str = Field(
        description="Resumo em 2 a 3 frases, dirigido ao candidato, sobre o quão adequado o seu perfil está para a vaga"
    )
    matched_skills: List[str] = Field(
        description="Skills/ferramentas pedidas na vaga que aparecem no currículo do candidato"
    )
    missing_skills: List[str] = Field(
        description="Skills/ferramentas pedidas na vaga que não aparecem no currículo do candidato"
    )
    strengths: List[str] = Field(
        description="Pontos do perfil do candidato que jogam a seu favor para esta vaga"
    )
    gaps: List[str] = Field(
        description="Lacunas do perfil do candidato face ao que a vaga pede (experiência, localização, skills, etc.)"
    )
