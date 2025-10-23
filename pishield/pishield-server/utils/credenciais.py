from database import db
import bcrypt

def salvar_credenciais(senha):
    credenciais = db['credenciais']

    credenciais.create_index('senha_hash', unique=True)

    existente = credenciais.find_one()

    if existente and bcrypt.checkpw(senha.encode(), existente['senha_hash'].encode()):
        return
    
    novo_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    if existente:
        credenciais.update_one({'_id': existente['_id']}, {'$set': {'senha_hash': novo_hash}})
        return
    
    credenciais.insert_one({'senha_hash': novo_hash})

def verificar_credenciais(senha):
    credenciais = db['credenciais']

    existente = credenciais.find_one()
    
    return bcrypt.checkpw(senha.encode(), existente['senha_hash'].encode())

def verificar_cliente(endereco):
    clientes = db['clientes']

    cliente = clientes.find_one({
        '$or': [
            {'endereco_ethernet': endereco},
            {'endereco_wifi': endereco}
        ]
    })

    return bool(cliente)
