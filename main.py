# main.py
# Ponto de entrada da aplicação.
from services.cv_parser_service import parse_cv_from_pdf
from services.vector_store_service import structured_cv_to_string


if __name__ == '__main__':
    file = 'eliseu_franco_cv.pdf'
    cv = parse_cv_from_pdf(file)

    print(structured_cv_to_string(cv)) # Retorna uma string pronta para gerar o embedding
