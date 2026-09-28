# services/pdf_service.py
# Responsável apenas pela leitura/extração de texto de ficheiros PDF.
import pypdf
from pathlib import Path


def extract_text_from_pdf(filename : str ) -> str:

    if not filename:
        raise FileNotFoundError("Ficheiro não encontrado ou vazio")

    if not Path(filename).exists():
        raise FileNotFoundError("Não encontramos o curriculo")

    try:
        reader = pypdf.PdfReader(filename, strict=False)
        cv_content = ''

        for content in reader.pages:
           cv_content += content.extract_text()

        if not cv_content:
            raise Exception("O connteúdo do curriculo não pode estar vazio")

        return cv_content

    except Exception:
        print("Houve um erro ao extrair dados do curriculo do candidato.") # Mudar depois para um adequado e bem tratado
        raise
