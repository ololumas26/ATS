# schemas/analysis_schema.py
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field


class AnalyzeForm(BaseModel):

    # str_strip_whitespace: rejeita descrições só com espaços
    # arbitrary_types_allowed: permite o UploadFile dentro do modelo
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    cv_file: UploadFile = Field(description="Currículo do candidato em PDF")
    job_description: str = Field(min_length=1, description="Descrição da vaga em texto livre")
