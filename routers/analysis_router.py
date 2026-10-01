# routers/analysis_router.py
# Recebe o currículo e a descrição da vaga no mesmo pedido.
import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException

from schemas.analysis_schema import AnalyzeForm
from services.cv_parser_service import parse_cv_from_pdf


router = APIRouter(tags=['analysis'])


@router.post('/analyze')
def analyze(data: Annotated[AnalyzeForm, Form()]):

    if data.cv_file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="O currículo deve ser um ficheiro PDF")

    # O parse_cv_from_pdf espera um caminho, por isso o upload é gravado num ficheiro temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        shutil.copyfileobj(data.cv_file.file, temp_file)
        temp_path = temp_file.name

    try:
        cv = parse_cv_from_pdf(temp_path)
    finally:
        Path(temp_path).unlink(missing_ok=True)

    return {'cv': cv, 'job_description': data.job_description}
