import os
import sys
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()  # Carrega variáveis do .env

def _is_valid_uri(uri: str) -> bool:
    from pymongo.uri_parser import parse_uri, InvalidURI
    try:
        parse_uri(uri)
        return True
    except InvalidURI:
        return False


def _validate_required(var_name: str, validator=lambda x: bool(x)) -> str | int:
    value = os.getenv(var_name)
    if not value or not validator(value):
        print(f'[ENV] Erro: a variável obrigatória "{var_name} está ausente ou inválida.')
        sys.exit(1)
    return value


@dataclass
class Env:
    '''
    Classe para armazenar as variáveis de ambiente do bot.
    '''
    AUTHORIZATION_TOKEN: str
    MAX_FILE_SIZE: int

    MONGO_URI: str | None = None
    CLUSTERS: dict[str, str] | None = None


    @classmethod
    def load(cls) -> 'Env':
        mongo_files = {
            key.removeprefix('MONGO_URI_FILES_').lower(): value
            for key, value in os.environ.items()
            if key.startswith('MONGO_URI_FILES_') and value and _is_valid_uri(value)
        }
        return cls(
            AUTHORIZATION_TOKEN=_validate_required('AUTHORIZATION'),
            MAX_FILE_SIZE=_validate_required('MAX_FILE_SIZE'),
            MONGO_URI=os.getenv('MONGO_URI'),
            CLUSTERS=mongo_files
        )

ENV = Env.load()
print(ENV.__dict__)