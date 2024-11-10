from ligar_connect import connection
import pandas as pd

"""
-- Tabela FUNCIONARIO (PAI)
CREATE TABLE Funcionario (
    Num_Reg INT PRIMARY KEY,
    Nome_Func VARCHAR(100)
);
"""
class Funcionario:
    def __init__(self, num_reg, nome_func):
        self.num_reg = num_reg
        self.nome_func = nome_func
        

    def inserir_funcionario(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
            cursor.execute(
                """
                INSERT INTO funcionario (Num_Reg, Nome_Func)
                VALUES (%s, %s);
                """,
                (self.num_reg, self.nome_func)
            )
            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Funcionario cadastrada com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao cadastrar o funcionario: {e}")
    
    @staticmethod
    def obter_funcionarios():
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Num_Reg, Nome_Func FROM Funcionario;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]  # Nome das colunas
            cursor.close()

            # Converter os dados para DataFrame do Pandas
            funcionarios_df = pd.DataFrame(rows, columns=colnames)
            return funcionarios_df

        except Exception as e:
            print(f"Erro ao obter funcionarios: {e}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro
    
    def editar_funcionario(self):
        try:
            cursor = connection.cursor() ## Ligar a conexão para fazer a inserção dos dados
        
            cursor.execute("""
                  UPDATE funcionario
                  SET Nome_Func = %s
                  WHERE Num_Reg = %s;
                """,
               (self.nome_func, self.num_reg)
            )
             # Verificar se o comando afetou alguma linha
            if cursor.rowcount == 0: #Isso tbm é mais para debugar (como sempre)
                print("Nenhuma linha foi atualizada - verifique se o Num_Reg existe.")

            connection.commit()
            cursor.close() ## Encerra a conexão
            print("Funcionario editado com sucesso!")
        except Exception as e:
            connection.rollback()  # Reverte a transação para limpar o erro
            print(f"Erro ao editar o funcionario: {e}")      
    
    
    def excluir_funcionario(num_reg):  
        try:
            cursor = connection.cursor()
            # Primeiro, excluir os registros dependentes das tabelas relacionadas - Não tem
    
            # Excluir da tabela 'Funcionario'
            cursor.execute(
                """
                DELETE FROM Funcionario WHERE Num_Reg = %s;
                """, (num_reg,)
            )
        
            connection.commit()
            cursor.close()
            
            print(f"Funcionario {num_reg} excluído com sucesso no banco de dados.")  # Debugar essa kralha
        except Exception as e:
            connection.rollback()
            print(f"Erro ao excluir o estado: {e}")
            print(f"Erro ao excluir o estado {num_reg}: {e}")  # tbm p debugar porra
    


