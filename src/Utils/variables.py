import os
from dotenv import load_dotenv

# Obtém o diretório do script
script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define o caminho para o arquivo .env
env_path = os.path.join(script_dir, '.env')

# Carrega o arquivo .env
load_dotenv(env_path)

def GetVariable(varibleName: str, default: str = None) -> str:
    variable = os.getenv(varibleName)
    if variable is None and default is not None: return default
    return variable