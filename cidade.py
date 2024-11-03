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
            cursor.execute("SELECT Nome_CID, codigo_CID, Preco_Unit_Valor, Preco_Unit_Peso, UF FROM Cidade;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]  # Nome das colunas
            cursor.close()

            # Converter os dados para DataFrame do Pandas
            cidades_df = pd.DataFrame(rows, columns=colnames)
            return cidades_df

        except Exception as e:
            print(f"Erro ao obter cidades: {e}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro


