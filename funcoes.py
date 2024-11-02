from ligar_connect import connection

def inserir_cliente(cod_cliente, data_insc, endereco, telefone, tipo_cliente):
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO cliente (Cod_Cli, Data_Insc, Endereco, Telefone, Tipo_Cliente)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (cod_cliente, data_insc, endereco, telefone, tipo_cliente)
        )
        connection.commit()
        cursor.close()
        print("Cliente cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar o cliente: {e}")
