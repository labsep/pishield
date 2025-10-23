from utils.rede import buscar_interfaces
from database.interfaces import atualizar_status_interfaces, obter_interfaces
from pprint import pprint

atualizar_status_interfaces(buscar_interfaces())

pprint(obter_interfaces())
