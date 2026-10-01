# routers/analysis_router.py
# Recebe o currículo e a descrição da vaga no mesmo pedido.
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException

from schemas.analysis_schema import AnalyzeForm
from services.analysis_orchestrator_service import AnalysisOrchestratorService


router = APIRouter(tags=['analysis'])


@router.post('/analyze')
def analyze(
    data: Annotated[AnalyzeForm, File()],  # File() faz o /docs declarar multipart/form-data
    orchestrator_service: AnalysisOrchestratorService = Depends(AnalysisOrchestratorService),
):

    try:
        return orchestrator_service.analyze(data.cv_file, data.job_description)

    except ValueError as e:
        # Erros de validação do serviço (ficheiro inválido, vazio, etc.) são erros do cliente
        raise HTTPException(status_code=400, detail=str(e))
