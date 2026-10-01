# services/openai_service.py
# Responsável apenas pela comunicação com a OpenAI.
import json

from openai import Client
from config.settings import OPENAI_API_KEY
from schemas.cv_schema import CurriculoEstruturado
from schemas.score_explanation_schema import ExplicacaoScore


client : Client = Client(api_key=OPENAI_API_KEY)


def extract_structured_cv_json(cv_content : str):

    if not cv_content or cv_content.strip() == '':
        raise FileNotFoundError("O conteúdo do email não pode estar vazio")

    schema_keys = [key for key in CurriculoEstruturado.model_fields.keys()]

    try: 
        response = client.responses.create(
            model='gpt-4o-mini',
            instructions="""
                    Você é um especialista em recrutamento e parsing de dados.
                    Extraia com precisão todas as informações do currículo fornecido
                """,
            input=cv_content,
            text={
                'format': {
                    'type':'json_schema',
                    'name': 'structured_cv',
                    'strict': True,
                    'schema': {
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': CurriculoEstruturado.model_json_schema()['properties'],
                        'required': schema_keys
                    } 
                }
            }
        )
        
        return response.output_text

    except Exception:
        print("Houve um erro ao obter a resposta da OPENAI") # Tratar adequadamente
        raise


def explain_score_json(cv : dict, job_description : str):

    if not job_description or job_description.strip() == '':
        raise ValueError("A descrição da vaga não pode estar vazia")

    schema_keys = [key for key in ExplicacaoScore.model_fields.keys()]

    try:
        response = client.responses.create(
            model='gpt-4o-mini',
            instructions="""
                    Você é um especialista em recrutamento que ajuda candidatos a perceber a sua adequação a uma vaga.
                    Compare o currículo estruturado do candidato com a descrição da vaga.
                    Escreva em português europeu, dirigindo-se diretamente ao candidato, num tom honesto e construtivo.
                    Baseie-se apenas no que está no currículo e na vaga; não invente experiência nem skills.
                """,
            input=f"Currículo do candidato (JSON):\n{json.dumps(cv, ensure_ascii=False)}\n\nDescrição da vaga:\n{job_description}",
            text={
                'format': {
                    'type':'json_schema',
                    'name': 'score_explanation',
                    'strict': True,
                    'schema': {
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': ExplicacaoScore.model_json_schema()['properties'],
                        'required': schema_keys
                    }
                }
            }
        )

        return response.output_text

    except Exception:
        print("Houve um erro ao obter a explicação do score da OPENAI") # Tratar adequadamente
        raise
