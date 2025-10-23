from database.escaneamentos import criar_escaneamento 
import xml.etree.ElementTree as ET
import subprocess
import requests
from dotenv import load_dotenv
import os
import time
import datetime
from ipaddress import IPv4Network
import json

load_dotenv()

def formatar_cpe(cpe):
    informacoes_cpe = cpe[5:].split(':') 
    informacoes_cpe = informacoes_cpe + [''] * (10 - len(informacoes_cpe))
    informacoes_cpe = [campo if campo else '*' for campo in informacoes_cpe]

    return 'cpe:2.3:' + ':'.join(informacoes_cpe)

def escanear_rede(endereco, prefixo):
    comando = ['nmap', '-sV', '-O', '-T4', f'{endereco}/{prefixo}', '-oX', '-']
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return ET.fromstring(resultado.stdout)

def obter_dispositivos_rede(rede):
    dispositivos = []

    for dispositivo in rede.findall('host'):
        dispositivos.append(dispositivo)

    return dispositivos

def obter_portas_dispositivo(dispositivo):
    portas = []

    for porta in dispositivo.findall('ports/port'):
        portas.append(porta)

    return portas

def obter_servicos_dispositivo(dispositivo):
    portas = obter_portas_dispositivo(dispositivo)

    servicos = []

    for porta in portas:
        servico = porta.find('service')
        if servico is not None:
            cpe = servico.find('cpe')
            if cpe is not None:
                cpe = cpe.text
                servicos.append(formatar_cpe(cpe))

    return servicos

def obter_endereco_dispositivo(dispositivo):
    for endereco in dispositivo.findall('address'):
        if endereco.get('addrtype') == 'mac':
            return endereco.get('addr')
        
def obter_endereco_rede_dispositivo(dispositivo):
    for endereco in dispositivo.findall('address'):
        if endereco.get('addrtype') == 'ipv4':
            return endereco.get('addr')

def obter_sistema_dispositivo(dispositivo):
    sistema = dispositivo.find('os')

    if sistema is None or not len(sistema):
        return None
    
    osmatch = sistema.find('osmatch')

    if osmatch is None or not len(osmatch):
        return None

    return osmatch.get('name')

def compilar_escaneamento(rede):
    escaneamento = {
        'endereco': str(rede.network_address),
        'mascara': str(rede.netmask),
        'cidr': str(rede.prefixlen),
        'dispositivos': {}
    }
    
    rede = escanear_rede(rede.network_address, rede.prefixlen)

    dispositivos = obter_dispositivos_rede(rede)

    for dispositivo in dispositivos:
        endereco_dispositivo = obter_endereco_dispositivo(dispositivo)

        escaneamento['dispositivos'][endereco_dispositivo] = {}

        escaneamento['dispositivos'][endereco_dispositivo]['endereco'] = endereco_dispositivo
        escaneamento['dispositivos'][endereco_dispositivo]['sistema'] = obter_sistema_dispositivo(dispositivo)
        escaneamento['dispositivos'][endereco_dispositivo]['endereco_rede'] = obter_endereco_rede_dispositivo(dispositivo)
        escaneamento['dispositivos'][endereco_dispositivo]['servicos'] = {}

        servicos = obter_servicos_dispositivo(dispositivo)

        for servico in servicos:
            escaneamento['dispositivos'][endereco_dispositivo]['servicos'][servico] = {
                'vulnerabilidades': {}
            }

    return escaneamento

if __name__ == '__main__':
    inicio = time.perf_counter()

    escaneamento_previo = compilar_escaneamento(IPv4Network('192.168.18.0/24'))

    resposta = requests.post(
        'http://127.0.0.1/api/vulnerabilidades',
        json={
            'escaneamento': escaneamento_previo
        }
    )

    escaneamento_completo = resposta.json()

    print(json.dumps(escaneamento_completo, ensure_ascii=False, indent=4))
    
    fim = time.perf_counter()

    print(f'Tempo: {fim-inicio:.2f} segundos')
