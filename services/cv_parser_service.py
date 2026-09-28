# services/cv_parser_service.py
# Orquestra o fluxo: PDF -> texto bruto -> OpenAI -> dicionário estruturado.
from schemas.cv_schema import CurriculoEstruturado
from services.pdf_service import extract_text_from_pdf
from services.openai_service import extract_structured_cv_json
from utils.json_utils import json_to_dict


def parse_cv_from_pdf(filename : str) -> CurriculoEstruturado:

    raw_cv_text = extract_text_from_pdf(filename)
    structured_cv_json = extract_structured_cv_json(raw_cv_text)
    return json_to_dict(structured_cv_json)
