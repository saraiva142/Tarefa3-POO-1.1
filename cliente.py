from ligar_connect import connection
import pandas as pd
import streamlit as st

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
    
    @staticmethod
    def obter_clientes():
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Cod_Cli, Data_Insc, Endereco, Telefone, Tipo_Cliente FROM Cliente;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]  # Nome das colunas
            cursor.close()

            # Converter os dados para DataFrame do Pandas
            clientes_df = pd.DataFrame(rows, columns=colnames)
            return clientes_df

        except Exception as e:
            print(f"Erro ao obter clientes: {e}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro
    
    @staticmethod
    def obter_pessoas_fisicas():
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Cod_Cli, Nome_Cli AS Nome, CPF
                FROM Pessoa_Fisica;
            """)
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            cursor.close()
            return pd.DataFrame(rows, columns=colnames)
        except Exception as e:
            print(f"Erro ao obter dados de pessoas físicas: {e}")
            return pd.DataFrame()

    @staticmethod
    def obter_pessoas_juridicas():
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Cod_Cli, Razao_Social, Insc_Estadual, CNPJ
                FROM Pessoa_Juridica;
            """)
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            cursor.close()
            return pd.DataFrame(rows, columns=colnames)
        except Exception as e:
            print(f"Erro ao obter dados de pessoas jurídicas: {e}")
            return pd.DataFrame()

    def editar_cliente(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            #print(f"Tentando editar cliente com ID: {self.cod_cliente}") mais debug de corno
            #print("Dados para atualização:", self.data_insc, self.endereco, self.telefone, self.tipo_cliente) # isso era para eu debugar o inferno
            
            #Não coloquei para editar o código do cliente pois ao meu ver não faz sentido

            cursor.execute("""
                  UPDATE cliente
                  SET Data_Insc = %s, Endereco = %s, Telefone = %s, Tipo_Cliente = %s
                  WHERE Cod_Cli = %s;
                """,
               (self.data_insc, self.endereco, self.telefone, self.tipo_cliente, self.cod_cliente)
            )
             # Verificar se o comando afetou alguma linha
            #print("Linhas afetadas pelo UPDATE:", cursor.rowcount) tava debugando, n aguento mais debugar essa desgraça
            if cursor.rowcount == 0: #Isso tbm é mais para debugar (como sempre)
                print("Nenhuma linha foi atualizada - verifique se o Cod_Cli existe.")

            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Cliente editado com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao editar o cliente: {e}")      
    
    @staticmethod
    def excluir_cliente(cod_cliente):  
        try:
            cursor = connection.cursor()
            # Primeiro, excluir os registros dependentes das tabelas relacionadas
            
            # Excluir da tabela 'Frete' onde o 'Destinatario_Cli' ou 'Remetente_Cli' seja o cod_cliente
            cursor.execute(
                """
                DELETE FROM Frete WHERE Destinatario_Cli = %s OR Remetente_Cli = %s;
                """, (cod_cliente, cod_cliente)
            )
            
            # Excluir da tabela 'Pessoa_Fisica' e 'Pessoa_Juridica' usando 'Cod_Cli'
            cursor.execute(
                """
                DELETE FROM Pessoa_Fisica WHERE Cod_Cli = %s;
                DELETE FROM Pessoa_Juridica WHERE Cod_Cli = %s;
                """, (cod_cliente, cod_cliente)
            )
            
            # Finalmente excluir o cliente da tabela 'cliente'
            cursor.execute(
                """
                DELETE FROM cliente WHERE Cod_Cli = %s;
                """, (cod_cliente,)
            )
        
            connection.commit()
            cursor.close()
            #st.success(f"Cliente {cod_cliente} excluído com sucesso!", icon="🤐")
            print(f"Cliente {cod_cliente} excluído com sucesso no banco de dados.")  # Debugar essa kralha
        except Exception as e:
            connection.rollback()
            st.error(f"Erro ao excluir o cliente: {e}")
            print(f"Erro ao excluir o cliente {cod_cliente}: {e}")  # tbm p debugar porra