from flask import Blueprint, request, jsonify, session
from database import db
from bson import ObjectId
import datetime
import re

clientes = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes.route('/')
def consultar_clientes():
    if 'administrador' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401

    consulta = db['clientes'].find().to_list()

    for documento in consulta:
        documento['_id'] = str(documento['_id'])
        documento['data'] = documento['data'].strftime('%Y/%m/%d, %H:%M:%S')

    return jsonify({'ok': True, 'mensagem': 'Dados retornados.', 'clientes': consulta}), 200

@clientes.route('/', methods=['POST'])
def cadastrar_cliente():
    if 'administrador' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    dados = request.json

    for parametro in ('endereco_ethernet', 'endereco_wifi'):
        if parametro not in dados:
            return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não especificado.'}), 400
        if not re.match('^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$', dados[parametro]):
            return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400

    colecao_clientes = db['clientes']
    
    colecao_clientes.insert_one({
        'endereco_ethernet': dados['endereco_ethernet'].upper(),
        'endereco_wifi': dados['endereco_wifi'].upper(),
        'data': datetime.datetime.now(tz=datetime.timezone.utc)
    })

    return jsonify({'ok': True, 'mensagem': 'Cliente cadastrado.'}), 201

@clientes.route('/<id>', methods=['DELETE'])
def deletar_cliente(id):
    if 'administrador' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    colecao_clientes = db['clientes']

    colecao_clientes.delete_one({'_id': ObjectId(id)})

    return jsonify({'ok': True, 'mensagem': 'Cliente deletado.'}), 200
