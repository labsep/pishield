from . import criar_conexao
import datetime

def obter_interface_padrao():
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM interfaces WHERE padrao = TRUE;')

    resultado = cursor.fetchone()

    conexao.close()

    return resultado

def obter_interfaces():
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM interfaces;')

    resultado = cursor.fetchall()

    conexao.close()

    return resultado

def atualizar_status_interfaces(interfaces_detectadas):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('UPDATE interfaces set ativa = FALSE;')

    try:
        for interface in interfaces_detectadas:
            cursor.execute(
                'INSERT IGNORE INTO interfaces VALUES (%s, %s, %s, %s, %s, %s, %s);',
                (
                    interface['endereco'],
                    interface['endereco_ipv4_rede'],
                    interface['prefixo'],
                    interface['nome'],
                    False,
                    True,
                    datetime.datetime.now()
                )
            )

            cursor.execute(
                'UPDATE interfaces SET ' \
                    'endereco_ipv4_rede = %s, ' \
                    'prefixo = %s, ' \
                    'nome = %s, ' \
                    'ativa = TRUE, ' \
                    'ultima_vez_vista = %s ' \
                'WHERE endereco = %s;',
                (
                    interface['endereco_ipv4_rede'],
                    interface['prefixo'],
                    interface['nome'],
                    datetime.datetime.now(),
                    interface['endereco']
                )
            )
    except Exception as e:
        print(e)
        conexao.rollback()
        conexao.close()
        return

    cursor.execute('SELECT ativa FROM interfaces WHERE padrao = TRUE;')

    padrao = cursor.fetchone()

    padrao_existe = padrao is not None

    padrao_ativa = padrao.get('ativa') if padrao else False

    if not (padrao_ativa and padrao_existe):
        cursor.execute('UPDATE interfaces SET padrao = FALSE;')

        cursor.execute('SELECT endereco FROM interfaces WHERE ativa = TRUE LIMIT 1;')

        endereco_nova_padrao = cursor.fetchone()['endereco']

        cursor.execute('UPDATE interfaces SET padrao = TRUE WHERE endereco = %s', (endereco_nova_padrao, ))

    conexao.commit()
    conexao.close()
