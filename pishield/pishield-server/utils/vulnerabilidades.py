import requests
from .referencias import pesquisar_referencias_vulnerabilidade
from .agente import Agente
from .navegador import Navegador
from config import instrucao
import os
import time

def pesquisar_cves(cpe):
    cves = {}

    try:
        pesquisa = requests.get(f'https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe}')
        pesquisa.raise_for_status()
    except:
        return None

    if not pesquisa.ok:
        return None
    
    json_pesquisa = pesquisa.json()
    vulnerabilidades = json_pesquisa['vulnerabilities']

    for vulnerabilidade in vulnerabilidades:
        vulnerabilidade = vulnerabilidade['cve']
        cves[vulnerabilidade['id']] = vulnerabilidade
    
    return cves

def processar_vulnerabilidade(vulnerabilidade):
    agente = Agente(os.environ.get('CHAVE_GEMINI'), instrucao)
    with Navegador() as navegador:
        pesquisar_referencias_vulnerabilidade(vulnerabilidade, navegador)

        while True:
            try:
                texto = agente.analisar_vulnerabilidade(vulnerabilidade)
                break
            except Exception as e:
                print(e)
                time.sleep(4)

        time.sleep(4)

        return texto
    