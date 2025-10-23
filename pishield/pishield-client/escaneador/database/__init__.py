import mariadb
import os
from dotenv import load_dotenv

load_dotenv()

def criar_conexao():
    return mariadb.connect(
        host=os.environ.get('BANCO_HOST'),
        port=int(os.environ.get('BANCO_PORTA')),
        user=os.environ.get('BANCO_USUARIO'),
        password=os.environ.get('BANCO_SENHA'),
        database=os.environ.get('BANCO_BANCO')
    )
