import mysql.connector
import requests
from mysql.connector import Error

try:
    conexao = mysql.connector.connect(host='localhost',
                                      database='db_cnpj',
                                      user='root',
                                      password='Magic1234')
    if conexao.is_connected():
        db_info = conexao.get_server_info()
        cursor = conexao.cursor()

    repetir_consulta = True

    while(repetir_consulta):
        opcao = int(input('\nPor favor, digite uma opção de naveção:'
                          '\n1 - Listar CNPJ cadastrados;'
                          '\n2 - Importar dados de CNPJ;\n'))

        if(opcao == 1):
            cursor.execute('SELECT * FROM tb_clientes;')
            linhas = cursor.fetchall()
            print(f'\nO banco de dados contém {cursor.rowcount} registros:\n')
            for linha in linhas:
                print(f'CNPJ: {linha[0]}\nRazão Social:{linha[1]}\n'
                      'Site: {linha[2]}\n')
            repetir_consulta = input('Digite "s" para voltar ao menu inicial'
                                     ' ou aperte qualquer tecla para sair do'
                                     ' programa.\n') == 's'

        elif(opcao == 2):
            repetir_cnpj = True
            while(repetir_cnpj):
                cnpj_digitado = input('\nPor favor, digite o CNPJ: ')
                if(cnpj_digitado == ''):
                    repetir_cnpj = input('O CNPJ informado é inválido, você'
                                         ' gostaria de fazer outra consulta?'
                                         '\nDigite "s" para sim ou aperte'
                                         ' qualquer tecla para voltar à tela'
                                         ' inicial:\n') == 's'
                else:
                    request = requests.get(f'https://www.receitaws.com.br/v1/cnpj/{cnpj_digitado}')
                    valida_cnpj = request.json()
                    if(valida_cnpj["status"] != 'ERROR'):
                        cnpj_bruto = valida_cnpj["cnpj"]
                        cnpj = '{}{}{}{}{}'.format(cnpj_bruto[:2], cnpj_bruto[2:5],
                                                          cnpj_bruto[5:8], cnpj_bruto[8:13], cnpj_bruto[13:])
                        razao_social = valida_cnpj["nome"]
                        site = 'Não informado'
                        print(f'CNPJ: {cnpj}')
                        print(f'Razão Social: {razao_social}')
                        print(f'Site: {site}\n')

                        criar_cliente = input("Você deseja criar um novo cliente com esses dados?"
                                              " Digite 's' para sim ou aperte qualquer outra tecla "
                                              "para voltar para a tela inicial.\n") == 's'
                        repetir_cnpj = False

                        if(criar_cliente):
                            try:
                                inserir_novo_cliente = f"INSERT INTO tb_clientes (cnpj, razao_social, site) VALUES " \
                                                       f"('{cnpj}', '{razao_social}', '{site}');"
                                cursor.execute(inserir_novo_cliente)
                                conexao.commit()
                            except Error as erro_cliente_cadastrado:
                                repetir_consulta = input('O cliente já encontra-se cadastrado. Digite "s" '
                                                         'para voltar ao menu inicial ou aperte qualquer tecla '
                                                         'para sair do programa.\n') == 's'
                    else:
                        repetir_cnpj = input('O CNPJ informado é inválido, você gostaria de fazer outra '
                                    'consulta?\nDigite "s" para sim ou aperte qualquer tecla '
                                             'para voltar à tela inicial:\n') == 's'

        else:
            print('Por favor, digite uma opção válida conforme abaixo:')

except Error as erro_conexao:
    print(f'Erro ao acessar tabela MySQL {erro_conexao}.')

finally:
    if(conexao.is_connected()):
        cursor.close()
        conexao.close()
        print('Obrigado por utilizar nosso programa.')
