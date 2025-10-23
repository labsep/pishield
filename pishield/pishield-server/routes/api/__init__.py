from flask import Blueprint
from .clientes import clientes
from .vulnerabilidades import vulnerabilidades

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(clientes)
api.register_blueprint(vulnerabilidades)