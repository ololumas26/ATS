import pypdf
import os
from pathlib import Path




def pdf_parser(filename : str):

    if not filename:
        raise FileNotFoundError("Ficheiro não encontrado")

    if not Path(filename):
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
        print("Houve um erro ao extrair dados do curriculo do candidato.")
        raise
        

filename = 'eliseu_franco_cv.pdf'

print(pdf_parser(filename))

# if not Path(filename).exists():
#     raise FileNotFoundError("Ficheiro não encontrado")


# reader = PdfReader(filename, strict=False)
# cv_content = ''

# for text in reader.pages:
#     t : str = text.extract_text()

#     print(t == '\n')
#     if t.strip() is not None or t != '\n':
#         cv_content += t
 

# print(cv_content)

