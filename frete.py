from ligar_connect import connection
import pandas as pd


class Frete:
    def __init__(self, num_conhec, peso, valor, pedagio, icms, data_frete, quem_paga, peso_ou_valor, origem_cid, destino_cid, remetente_cli, destinatario_cli):
        self.num_conhec = num_conhec
        self.peso = peso
        self.valor = valor
        self.pedagio = pedagio
        self.icms = icms
        self.data_frete = data_frete
        self.quem_paga = quem_paga
        self.peso_ou_valor = peso_ou_valor
        self.origem_cid = origem_cid
        self.destino_cid = destino_cid
        self.remetente_cli = remetente_cli
        self.destinatario_cli = destinatario_cli

    def inserir_frete(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            cursor.execute(
                """
                INSERT INTO frete (Num_Conhec, Peso, Valor, Pedagio, ICMS, Data_Frete, Quem_Paga, Peso_Ou_Valor, Origem_CID, Destino_CID, Remetente_Cli, Destinatario_Cli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (self.num_conhec, self.peso, self.valor, self.pedagio, self.icms, self.data_frete, self.quem_paga, self.peso_ou_valor, self.origem_cid, self.destino_cid, self.remetente_cli, self.destinatario_cli)
            )
            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Frete cadastrado com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao cadastrar o frete: {e}")
              
    @staticmethod
    def obter_fretes():
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Num_Conhec, Peso, Valor, Pedagio, ICMS, Data_Frete, Quem_Paga, Peso_Ou_Valor, Origem_CID, Destino_CID, Remetente_Cli, Destinatario_Cli FROM Frete;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]  # Nome das colunas
            cursor.close()

            # Converter os dados para DataFrame do Pandas
            fretes_df = pd.DataFrame(rows, columns=colnames)
            return fretes_df

        except Exception as e:
            print(f"Erro ao obter fretes: {e}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

    @staticmethod
    def excluir_fretes(num_conhec):
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM Frete WHERE Num_Conhec = %s;
                """, (num_conhec,)
            )

            connection.commit()
            cursor.close()

            print(f"Frete {num_conhec} excluído com sucesso no banco de dados.")
        except Exception as e:
            connection.rollback()

            print(f"Erro ao excluir o frete {num_conhec}: {e}")


    def editar_frete(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
          
            cursor.execute("""
                  UPDATE Frete
                  SET Peso = %s, Valor = %s, Pedagio = %s, ICMS = %s, Data_Frete = %s, Quem_Paga = %s, Peso_Ou_Valor = %s, Origem_CID = %s, Destino_CID = %s, Remetente_Cli = %s, Destinatario_Cli = %s
                  WHERE Num_Conhec = %s;
                """,
               (self.peso, self.valor, self.pedagio, self.icms, self.data_frete, self.quem_paga, self.peso_ou_valor, self.origem_cid, self.destino_cid, self.remetente_cli, self.destinatario_cli, self.num_conhec)
            )
             # Verificar se o comando afetou alguma linha
            #print("Linhas afetadas pelo UPDATE:", cursor.rowcount) tava debugando, n aguento mais debugar essa desgraça
            if cursor.rowcount == 0: #Isso tbm é mais para debugar (como sempre)
                print("Nenhuma linha foi atualizada - verifique se o Num Conhecimento existe.")

            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Frete editado com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao editar o frete: {e}")     

    #Fase 3
    @staticmethod
    def obter_arrecadacao_por_cidade_estado(uf, cidade):
        try:
            cursor = connection.cursor()  # Ligando a conexão
            
            cursor.execute("""
                SELECT 
                    c.nome_cid AS cidade_destino, 
                    c.uf AS uf_destino, 
                    COUNT(f.Num_Conhec) AS quantidade_fretes, 
                    SUM(f.Valor) AS total_arrecadado
                FROM Frete f
                JOIN Cidade c ON f.Destino_CID = c.Codigo_CID
                WHERE c.uf = %s AND c.nome_cid = %s AND EXTRACT(YEAR FROM f.Data_Frete) = 2024
                GROUP BY c.nome_cid, c.uf;
            """, (uf, cidade))
            
            resultado = cursor.fetchall()  # Obtendo os resultados da consulta
            
            cursor.close()  # Encerrando o cursor
            return resultado
        
        except Exception as e:
            connection.rollback()  # Revertendo em caso de erro
            print(f"Erro ao obter arrecadação: {e}")
            return []

        