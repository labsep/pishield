from . import criar_conexao

def criar_escaneamento(data_hora, endereco_interface):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('INSERT IGNORE INTO escaneamentos (data_hora, endereco_interface) VALUES (%s, %s);', (data_hora, endereco_interface))

    conexao.commit()
    conexao.close()

