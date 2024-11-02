from ligar_connect import connection

class Cliente:
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
    
    def inserir_pessoa_fisica(self, nome, cpf):
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Pessoa_Fisica (Cod_Cli, Nome_Cli, CPF)
                VALUES (%s, %s, %s);
                """,
                (self.cod_cliente, nome, cpf)
            )
            connection.commit()
            cursor.close()
            print("Pessoa Física cadastrada com sucesso!")
        
        except Exception as e:
            connection.rollback()
            print(f"Erro ao cadastrar a pessoa física: {e}")

    def inserir_pessoa_juridica(self, razao_social, insc_estadual, cnpj):
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Pessoa_Juridica (Cod_Cli, Razao_Social, Insc_Estadual, CNPJ)
                VALUES (%s, %s, %s, %s);
                """,
                (self.cod_cliente, razao_social, insc_estadual, cnpj)
            )
            connection.commit()
            cursor.close()
            print("Pessoa Jurídica cadastrada com sucesso!")
        
        except Exception as e:
            connection.rollback()
            print(f"Erro ao cadastrar a pessoa jurídica: {e}")

