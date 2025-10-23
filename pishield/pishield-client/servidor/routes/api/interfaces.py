from flask import Blueprint
from database import db

interfaces = Blueprint('interfaces', __name__, url_prefix='/interfaces')

@interfaces.route('/', methods=['GET'])
def consultar_interfaces():
    colecao_interfaces = db['interfaces']

    lista_interfaces = colecao_interfaces.find({})