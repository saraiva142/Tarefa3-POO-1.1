import psycopg2 as pg
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

def conn():
    try:
        pwd = os.getenv("DB_PASSWORD")
        conecta = pg.connect (
            user = "postgres",
            password = pwd,
            host = "localhost",
            port = 5433,
            database = "postgres"
        )
        
        print("Conectado com sucesso!!!!")
        
        return conecta
    
    except Error as e:
        print(f"Ocorreu um erro ao tentar conectar com o banco de dados  {e}")
        
def encerra_conn(conecta):
    if conecta:
        conecta.close()