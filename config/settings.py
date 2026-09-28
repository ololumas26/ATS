# config/settings.py
# Carrega as variáveis de ambiente (.env) e expõe as configurações da aplicação.
import os
from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
