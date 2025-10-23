from flask import Blueprint, request, jsonify
from utils.vulnerabilidades import pesquisar_cves, processar_vulnerabilidade
from config import instrucao

vulnerabilidades = Blueprint('vulnerabilidades', __name__, url_prefix='/vulnerabilidades')

@vulnerabilidades.route('/', methods=['POST'])
def compilar_vulnerabilidades():
    print(instrucao)

    dados = request.json

    if 'escaneamento' not in dados:
        return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não especificado.'}), 400
    
    escaneamento = dados['escaneamento']
    
    dispositivos = escaneamento['dispositivos']

    for dispositivo in dispositivos:
        servicos = dispositivos[dispositivo]['servicos']

        for servico in servicos:
            vulnerabilidades_servico = pesquisar_cves(servico)

            print(vulnerabilidades_servico)

            if not vulnerabilidades_servico:
                continue

            for vulnerabilidade in vulnerabilidades_servico:
                texto_vulnerabilidade = processar_vulnerabilidade(
                    vulnerabilidades_servico[vulnerabilidade]
                )
                
                dispositivos[dispositivo]['servicos'][servico]['vulnerabilidades'][vulnerabilidade] = texto_vulnerabilidade

    return jsonify(escaneamento)

