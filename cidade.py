from ligar_connect import connection
import pandas as pd

class Cidade:
    def __init__(self, nome_cid, codigo_cid, preco_unit_valor, preco_unit_peso, uf):
        self.nome_cid = nome_cid
        self.codigo_cid = codigo_cid
        self.preco_unit_valor = preco_unit_valor
        self.preco_unit_peso = preco_unit_peso
        self.uf = uf
        

    def inserir_cidade(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            cursor.execute(
                """
                INSERT INTO cidade (Nome_CID, codigo_CID, Preco_Unit_Valor, Preco_Unit_Peso, UF)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (self.nome_cid, self.codigo_cid, self.preco_unit_valor, self.preco_unit_peso, self.uf)
            )
            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Cidade cadastrada com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao cadastrar a cidade: {e}")
    
    @staticmethod
    def obter_cidades():
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT Nome_CID, codigo_CID, Preco_Unit_Valor, Preco_Unit_Peso, UF FROM Cidade;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]  # Nome das colunas
            cursor.close()

            # Converter os dados para DataFrame do Pandas
            cidades_df = pd.DataFrame(rows, columns=colnames)
            return cidades_df

        except Exception as e:
            print(f"Erro ao obter cidades: {e}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

    def editar_cidade(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            #print(f"Tentando editar cliente com ID: {self.cod_cliente}") mais debug de corno
            #print("Dados para atualização:", self.data_insc, self.endereco, self.telefone, self.tipo_cliente) # isso era para eu debugar o inferno
            
            #Não coloquei para editar o código do cliente pois ao meu ver não faz sentido

            cursor.execute("""
                  UPDATE cidade
                  SET Nome_CID = %s, Preco_Unit_Valor = %s, Preco_Unit_Peso = %s, UF = %s
                  WHERE codigo_CID = %s;
                """,
               (self.nome_cid, self.preco_unit_valor , self.preco_unit_peso , self.uf, self.codigo_cid)
            )
             # Verificar se o comando afetou alguma linha
            #print("Linhas afetadas pelo UPDATE:", cursor.rowcount) tava debugando, n aguento mais debugar essa desgraça
            if cursor.rowcount == 0: #Isso tbm é mais para debugar (como sempre)
                print("Nenhuma linha foi atualizada - verifique se o codigo_cid existe.")

            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Cidade editada com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao editar a cidade: {e}") 

    @staticmethod
    def excluir_cidade(codigo_cid):  
        try:
            cursor = connection.cursor()
            # Primeiro, excluir os registros dependentes das tabelas relacionadas
            
            # Excluir da tabela 'Frete' onde o 'Origem_Cid' ou 'Destino_Cid' seja o codigo_cidade
            cursor.execute(
                """
                DELETE FROM Frete WHERE Origem_CID = %s OR Destino_CID = %s;
                """, (codigo_cid, codigo_cid)
            )
            
            cursor.execute(
                """
                DELETE FROM Cidade WHERE codigo_cid = %s;
                """, (codigo_cid,)
            )
            
            connection.commit()
            cursor.close()
            
            print(f"Cidade {codigo_cid} excluída com sucesso no banco de dados.")  # Debugar essa kralha
        except Exception as e:
            connection.rollback()
            
            print(f"Erro ao excluir a cidade {codigo_cid}: {e}")  # tbm p debugar porra