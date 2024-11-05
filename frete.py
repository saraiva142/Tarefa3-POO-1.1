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