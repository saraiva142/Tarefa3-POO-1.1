
# Trabalho 3 de POO em Banco de Dados :game_die:

### É um trabalho onde desenvolvemos uma aplicação conectada a um banco de dados postgres, o qual com uma interface baseada em streamlit podemos fazer o CRUD das tabelas em relação ao contexto do exercício.

#### Bibliotecas para serem instaladas:

```sh
pip install streamlit
```
```sh
pip install psycopg2
```
```sh
pip install python-dotenv
```

#### Para Rodar :

1- Ligar o Docker
Se precisar criar outro Docker esse é o comando:
```sh
docker run --name my-postgres -e POSTGRES_PASSWORD=my*****password -p 5433:5432 -d postgres:latest
```
2- Abrir o Postrges no Dbear e vê se está conectado e se as tabelas estão normais
Se precisar fazer a criação das tabelas, utilizar o arquivo `Script`

3- Rodar o arquivo ligar_connect na pasta services, para conectar com o postgres

## Arquivos:

`main.py`: Parte destinada para o streamlit, onde é responsável pela interface e I/O do projeto. Nele estão construídos os formulários para fazer o CRUD dos itens das tabelas, nos formulários são chamados as funções de inserção/seleção/delete/update do arquivo `função.py` onde está os referentes sripts/querys.

`funcao.py`: Esse arquivo é destinado para a criação das funções de scripts/querys que serão feitas no banco de dados.

`connect.py`: É o arquivo responsável por configurar a conexão do projeto com o banco de dados postgres, onde é usado a biblioteca `psycopg2` que possui o `psycopg2.connect` para a configuração, configuração essa tendo em base como foi configurado o Docker para rodar o postgres.

`.env`: Esse arquivo é usado para garantir uma melhor segurança sobre a senha para acessar o banco de dados, onde é passada essa senha e no arquivo de configuração da conexão (`connect.py`) quando for passado a senha, ela é referenciada pelo `load_dotenv` da biblioteca `dotenv`. Assim, quem tiver acesso ao arquivo `connect.py` não terá acesso a essa senha.

`ligar_connect`: Esse arquivo não está sendo usado, pois a conexão está sendo ligada a cada função de script/query do arquivo `funcao.py`. Porém está no projeto para se caso precisarmos ligar manualmente para debugs.

`Script`: Arquivo dos SQL para a criação do database (*LEMBRAR DE COLOCAR*)

### Banco de Dados:

![image](https://github.com/user-attachments/assets/d019e090-3a87-4fcd-89e9-53d906a4516b)



:construction: EM CONSTRUÇÃO :construction: