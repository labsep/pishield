from config import referencias_por_vulnerabilidade

def pesquisar_referencias_vulnerabilidade(vulnerabilidade, navegador, referencias_por_vulnerabilidade=referencias_por_vulnerabilidade):
    for i, referencia in enumerate(vulnerabilidade['references']):
            if i == referencias_por_vulnerabilidade: break

            url = referencia['url']

            try:
                pesquisar_referencia(vulnerabilidade, i, url, navegador)
            except:
                continue

def pesquisar_referencia(vulnerabilidade, id_referencia, url, navegador):
    resultado = navegador.pesquisar(url)

    vulnerabilidade['references'][id_referencia]['content'] = resultado
    