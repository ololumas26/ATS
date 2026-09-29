# services/openai_service.py
# Responsável apenas pela comunicação com a OpenAI.
from openai import Client
from config.settings import OPENAI_API_KEY
from schemas.cv_schema import CurriculoEstruturado


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
