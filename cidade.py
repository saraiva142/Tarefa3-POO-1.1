from ligar_connect import connection

class Cidade:
    def __init__(self, cod_cliente, data_insc, endereco, telefone, tipo_cliente):
        self.cod_cliente = cod_cliente
        self.data_insc = data_insc
        self.endereco = endereco
        self.telefone = telefone
        self.tipo_cliente = tipo_cliente

    def inserir_cliente(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            cursor.execute(
                """
                INSERT INTO cliente (Cod_Cli, Data_Insc, Endereco, Telefone, Tipo_Cliente)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (self.cod_cliente, self.data_insc, self.endereco, self.telefone, self.tipo_cliente)
            )
            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Cliente cadastrado com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao cadastrar o cliente: {e}")

