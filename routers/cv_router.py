# routers/cv_router.py
# Endpoints relacionados com currículos.
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from services.cv_parser_service import parse_cv_from_pdf


router = APIRouter(prefix='/cv', tags=['cv'])


@router.post('/upload')
def upload_cv(cv_file: UploadFile = File(...)):

    if cv_file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="O currículo deve ser um ficheiro PDF")

    # O parse_cv_from_pdf espera um caminho, por isso o upload é gravado num ficheiro temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        shutil.copyfileobj(cv_file.file, temp_file)
        temp_path = temp_file.name
        print("Ficheiro na memória: ", temp_path)

    try:
        return parse_cv_from_pdf(temp_path)
    finally:
        Path(temp_path).unlink(missing_ok=True)
