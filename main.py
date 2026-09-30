# main.py
# Ponto de entrada da aplicação.
from services.cv_parser_service import parse_cv_from_pdf
from services.vector_store_service import(
    structured_cv_to_string,
    gen_embedding_from_text,
    structured_job_to_string
) 
from services.qdrant_service import qclient, CV_COLLECTION_NAME
from qdrant_client.models import PointStruct



if __name__ == '__main__':

    fake_job = {
    'job_title': 'Backend Developer (Python)',
    'company_name': 'Nzila Tech',
    'job_location': 'Luanda, Angola (híbrido)',
    'required_skills': [
        'Python', 'FastAPI', 'PostgreSQL', 'Docker',
        'REST APIs', 'Git', 'SQL'
    ],
    'min_experience_years': 2,
    'job_description': (
        'Procuramos um Backend Developer para integrar a equipa de produto de uma '
        'fintech em crescimento. A pessoa será responsável por desenhar e manter '
        'APIs REST em FastAPI, modelar dados em PostgreSQL e colaborar com a equipa '
        'de frontend na entrega de funcionalidades ponta a ponta. Valorizamos '
        'autonomia, boas práticas de código e experiência com Docker em ambientes '
        'de produção.'
    ),
}


    
    file = 'eliseu_franco_cv.pdf'
    cv = parse_cv_from_pdf(file)
    stuctured = structured_cv_to_string(cv)
    job_embedding = gen_embedding_from_text(structured_job_to_string(fake_job))
    

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

    result = qclient.query_points(
        collection_name='first_collection',
        query=job_embedding,
        limit=5
    )

    print("Resultado da busca: ", result)
    qclient.close()
