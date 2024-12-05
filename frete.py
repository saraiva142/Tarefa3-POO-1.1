from ligar_connect import connection
import pandas as pd


class Frete:
    def __init__(self, num_conhec, peso, valor, pedagio, icms, data_frete, quem_paga, peso_ou_valor, origem_cid, destino_cid, remetente_cli, destinatario_cli, funcionario):
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
        self.funcionario = funcionario

    def inserir_frete(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            cursor.execute(
                """
                INSERT INTO frete (Num_Conhec, Peso, Valor, Pedagio, ICMS, Data_Frete, Quem_Paga, Peso_Ou_Valor, Origem_CID, Destino_CID, Remetente_Cli, Destinatario_Cli, Funcionario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (self.num_conhec, self.peso, self.valor, self.pedagio, self.icms, self.data_frete, self.quem_paga, self.peso_ou_valor, self.origem_cid, self.destino_cid, self.remetente_cli, self.destinatario_cli, self.funcionario)
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
            cursor.execute("SELECT Num_Conhec, Peso, Valor, Pedagio, ICMS, Data_Frete, Quem_Paga, Peso_Ou_Valor, Origem_CID, Destino_CID, Remetente_Cli, Destinatario_Cli, Funcionario FROM Frete;")
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
                SET Peso = %s, Valor = %s, Pedagio = %s, ICMS = %s, Data_Frete = %s, Quem_Paga = %s, Peso_Ou_Valor = %s, Origem_CID = %s, Destino_CID = %s, Remetente_Cli = %s, Destinatario_Cli = %s, Funcionario = %s
                WHERE Num_Conhec = %s;
                """,
            (self.peso, self.valor, self.pedagio, self.icms, self.data_frete, self.quem_paga, self.peso_ou_valor, self.origem_cid, self.destino_cid, self.remetente_cli, self.destinatario_cli, self.funcionario, self.num_conhec)
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
            
        
            # Processar os resultados para retornar como lista de dicionários
            #Ou seja, conceito de Collections
            dados_processados = []
            for row in resultado:
                dados_processados.append({
                    "cidade_destino": row[0],
                    "uf_destino": row[1],
                    "quantidade_fretes": row[2],
                    "total_arrecadado": row[3]
                })

            return dados_processados  # Retorna como uma lista de dicionários => COLLECTIONS

        
        except Exception as e:
            connection.rollback()  # Revertendo em caso de erro
            print(f"Erro ao obter arrecadação: {e}")
            return []

    @staticmethod
    @staticmethod
    def obter_fretes_funcionarios_pj(mes_ano):
        try:
            # Dividir o mês e o ano fornecidos
            mes, ano = map(int, mes_ano.split('/'))
            
            print(f"Buscando fretes para: {mes}/{ano}")  #Apenas para debugar

            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT 
                    f.Num_Conhec AS num_conhecimento,
                    f.Data_Frete AS data_frete,
                    pj.Razao_Social AS representante_empresa, -- Razão social da pessoa jurídica
                    func.Nome_Func AS funcionario_responsavel
                FROM Frete f
                JOIN Cliente c ON f.Destinatario_Cli = c.Cod_Cli
                JOIN Pessoa_Juridica pj ON c.Cod_Cli = pj.Cod_Cli
                JOIN Funcionario func ON f.Funcionario = func.Num_Reg
                WHERE c.Tipo_Cliente = 'Pessoa Juridica' -- Apenas PJ
                AND EXTRACT(MONTH FROM f.Data_Frete) = %s
                AND EXTRACT(YEAR FROM f.Data_Frete) = %s;
            """, (mes, ano))
            
            resultado = cursor.fetchall()
            cursor.close()
            
            print(f"Resultado da consulta: {resultado}")  #Socorro ta bugado
            
             # Depurando o filha da puta q n funciona
            if not resultado:
                print(f"Nenhum frete encontrado para {mes}/{ano}")
                
            # Processar resultados em formato de lista de dicionários
            fretes_processados = [
                {
                    "num_conhecimento": row[0],
                    "data_frete": row[1],
                    "representante_empresa": row[2],
                    "funcionario_responsavel": row[3],
                }
                for row in resultado
            ]
            
            return fretes_processados

        except Exception as e:
            connection.rollback()
            print(f"Erro ao buscar fretes: {e}")
            return []

    @staticmethod
    def obter_media_fretes_por_cidade_estado(estado):
        try:
            cursor = connection.cursor()  # Ligando a conexão
        
            cursor.execute("""
                SELECT  
                    c.uf AS estado,
                    c.nome_cid AS cidade,
                    AVG(CASE WHEN f.Origem_CID = c.Codigo_CID THEN 1.0 ELSE 0.0 END) AS media_fretes_origem,
                    AVG(CASE WHEN f.Destino_CID = c.Codigo_CID THEN 1.0 ELSE 0.0 END) AS media_fretes_destino
                FROM Cidade c
                LEFT JOIN Frete f 
                    ON f.Origem_CID = c.Codigo_CID OR f.Destino_CID = c.Codigo_CID
                WHERE c.uf = %s
                GROUP BY c.uf, c.nome_cid
                ORDER BY c.nome_cid;

            """, (estado,))

            # Obter os resultados da consulta
            resultado = cursor.fetchall()
            cursor.close()

            print(f"Resultado da consulta: {resultado}")  # Para debugar o que foi retornado

            # Se não encontrar dados, retorna uma lista vazia
            if not resultado:
                print(f"Nenhum dado encontrado para o estado {estado}")
                return []

            # Processar resultados em formato de lista de dicionários
            fretes_processados = [
                {
                    "estado": row[0],
                    "cidade": row[1],
                    "media_fretes_origem": row[2],
                    "media_fretes_destino": row[3],
                }
                for row in resultado
            ]
            
            return fretes_processados

        except Exception as e:
            # Em caso de erro, reverte qualquer transação pendente e imprime a mensagem de erro
            print(f"Erro ao buscar dados: {e}")
            return []