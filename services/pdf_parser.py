import pypdf
from pathlib import Path
from openai import Client, OpenAI
import os
from dotenv import load_dotenv
from schema import CurriculoEstruturado
from functools import lru_cache


load_dotenv()


openai_key = os.environ.get('OPENAI_KEY')
client : Client = Client(api_key=openai_key)

def get_openai_response(cv_content : str):

    if not cv_content or cv_content.strip() == '':
        raise FileNotFoundError("O conteúdo do email não pode estar vazio")

    schema_keys = [key for key in CurriculoEstruturado.model_fields.keys()]

    try: 
        response = client.responses.create(
            model='gpt-4o-mini',
            instructions="""
                        Você é um especialista em recrutamento e parsing de dados. Extraia com precisão todas as informações do currículo fornecido
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

    
    



def pdf_parser(filename : str ) -> str:

    if not filename:
        raise FileNotFoundError("Ficheiro não encontrado ou vazio")

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
        print("Houve um erro ao extrair dados do curriculo do candidato.") # Mudar depois para um adequado e bem tratado
        raise


def strutured_cv(filename : str) -> CurriculoEstruturado:

    gross_content = pdf_parser(filename)
    strutured_content = get_openai_response(gross_content)
    return strutured_content


