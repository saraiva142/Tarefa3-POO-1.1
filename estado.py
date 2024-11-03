from ligar_connect import connection
import pandas as pd

class Estado:
    def __init__(self, uf, icms_local, nome_est, icms_outro_uf):
        self.uf = uf
        self.icms_local = icms_local
        self.nome_est = nome_est
        self.icms_outro_uf = icms_outro_uf

    def inserir_estado(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            cursor.execute(
                """
                INSERT INTO estado (UF, ICMS_Local, Nome_Est, ICMS_Outro_UF)
                VALUES (%s, %s, %s, %s);
                """,
                (self.uf, self.icms_local, self.nome_est, self.icms_outro_uf)
            )
            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Estado cadastrado com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao cadastrar o estado: {e}")
    
    @staticmethod
    def obter_estados():
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT UF, ICMS_Local, Nome_Est, ICMS_Outro_UF FROM Estado;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]  # Nome das colunas
            cursor.close()

            # Converter os dados para DataFrame do Pandas
            estados_df = pd.DataFrame(rows, columns=colnames)
            return estados_df

        except Exception as e:
            print(f"Erro ao obter estados: {e}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro
