from connect import conn

connection = conn()

def encerra_conn():
    if connection:
        connection.close()
        print("Conexão encerrada com sucesso.")
