from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.credenciais import verificar_credenciais

home = Blueprint('home', __name__, url_prefix='/')

@home.route('/')
def home_handler():
    if 'administrador' not in session:
        return redirect(url_for('home.login'))

    return render_template('index.html')

@home.route('/login')
def login():
    return render_template('login.html')

@home.route('/login', methods=['POST'])
def verificar_login():
    dados = request.json

    if 'senha' not in dados:
        return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não especificado.'}), 400
    
    if not verificar_credenciais(dados['senha']):
        return jsonify({'ok': False, 'mensagem': 'Senha incorreta.'}), 401
    
    session['administrador'] = True

    return jsonify({'ok': True, 'mensagem': 'Autenticado com sucesso.'}), 200
