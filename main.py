# main.py
# Ponto de entrada da aplicação.
from services.cv_parser_service import parse_cv_from_pdf
from services.vector_store_service import structured_cv_to_string


if __name__ == '__main__':
    file = 'eliseu_franco_cv.pdf'
    
    # file = 'eliseu_franco_cv.pdf'
    # cv = parse_cv_from_pdf(file)
    # stuctured = structured_cv_to_string(cv)
    # embedding = gen_embedding_from_text(stuctured)

    # qclient.upsert(
    #     collection_name=CV_COLLECTION_NAME,
    #     points=[
    #         PointStruct(
    #             id=1,
    #             vector=embedding,
    #             payload={
    #                 'name': 'Eliseu Samulolo', 'texto': 'texto livre do curriculo'
    #             }
    #         )
    #     ]
    # )

    # qclient.close()