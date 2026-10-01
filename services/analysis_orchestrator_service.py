# services/analysis_orchestrator_service.py
# Orquestra a análise: CV (PDF) + descrição da vaga -> score de compatibilidade.
import shutil
import tempfile
from pathlib import Path

from fastapi import UploadFile

from services.cv_parser_service import parse_cv_from_pdf
from services.vector_store_service import structured_cv_to_string, gen_embedding_from_text
from services.calc_cossin_service import CosineSimilarity
from services.openai_service import explain_score_json
from utils.json_utils import json_to_dict


class AnalysisOrchestratorService:

    def save_cv_to_temp_file(self, cv_file : UploadFile) -> str:

        if cv_file is None:
            raise ValueError("Nenhum currículo foi enviado")

        if cv_file.content_type != 'application/pdf':
            raise ValueError("O currículo deve ser um ficheiro PDF")

        if not cv_file.filename or not cv_file.filename.lower().endswith('.pdf'):
            raise ValueError("O ficheiro do currículo deve ter a extensão .pdf")

        # O parse_cv_from_pdf espera um caminho, por isso o upload é gravado num ficheiro temporário
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            shutil.copyfileobj(cv_file.file, temp_file)
            cv_path = temp_file.name

        if Path(cv_path).stat().st_size == 0:
            Path(cv_path).unlink(missing_ok=True)
            raise ValueError("O ficheiro do currículo está vazio")

        return cv_path

    def analyze(self, cv_file : UploadFile, job_description : str) -> dict:

        cv_path = self.save_cv_to_temp_file(cv_file)

        try:
            cv = parse_cv_from_pdf(cv_path)
        finally:
            Path(cv_path).unlink(missing_ok=True)

        cv_embedding = gen_embedding_from_text(structured_cv_to_string(cv))
        job_embedding = gen_embedding_from_text(job_description)

        score = CosineSimilarity(cv_embedding, job_embedding).calc_cossin_similarity()

        explanation = json_to_dict(explain_score_json(cv, job_description))

        return {'cv': cv, 'score': score, 'explanation': explanation}



