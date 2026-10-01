# routers/analysis_router.py
# Recebe o currículo e a descrição da vaga no mesmo pedido.
import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Depends

from schemas.analysis_schema import AnalyzeForm
from services.cv_parser_service import parse_cv_from_pdf

from services.analysis_orchestrator_service import AnalysisOrchestratorService


router = APIRouter(tags=['analysis'])


@router.post('/analyze')
def analyze(data: Annotated[AnalyzeForm, File()],
        orchestror_service : AnalysisOrchestratorService = Depends(AnalysisOrchestratorService)):  # File() faz o /docs declarar multipart/form-data

        response = orchestror_service.analyze(data.cv_file, data.job_description)

        return response
