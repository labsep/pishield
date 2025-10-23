import psutil
import socket
import ipaddress
from netaddr import IPNetwork

def obter_prefixo(endereco, mascara):
    return IPNetwork(f'{endereco}/{mascara}').prefixlen

def validar_interface(nome_interface):
    nome = nome_interface.lower()

    return (
        nome.startswith('eth') or
        nome.startswith('en') or
        nome.startswith('wl') or 
        nome.startswith('wifi') or
        nome.startswith('wi-fi')
    )

def buscar_interfaces():
    lista_interfaces = psutil.net_if_addrs()

    interfaces = []

    for interface in lista_interfaces:
        if not validar_interface(interface):
            continue

        familias = [familia.family for familia in lista_interfaces[interface]]

        if not (socket.AF_INET in familias and psutil.AF_LINK in familias):
            continue

        familia_ipv4 = [familia for familia in lista_interfaces[interface] if familia.family == socket.AF_INET][0]
        familia_mac = [familia for familia in lista_interfaces[interface] if familia.family == psutil.AF_LINK][0]

        prefixo = obter_prefixo(familia_ipv4.address, familia_ipv4.netmask)

        rede = ipaddress.IPv4Network(f'{familia_ipv4.address}/{prefixo}', strict=False)
        interfaces.append({
            'nome': interface,
            'endereco_ipv4_rede': str(rede.network_address),
            'prefixo': prefixo,
            'endereco': familia_mac.address
        })
        
    return interfaces
