-- COMANDO PARA CONECTAR DOCKER: docker run --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5433:5432 -d --rm postgres:latest

-- Tabela ESTADO
CREATE TABLE Estado (
    UF CHAR(2) PRIMARY KEY,
    ICMS_Local DECIMAL(10, 2),
    Nome_Est VARCHAR(100),
    ICMS_Outro_UF DECIMAL(10, 2)
);

-- Tabela CIDADE
CREATE TABLE Cidade (
    Codigo_CID INT PRIMARY KEY,
    Nome_CID VARCHAR(100),
    UF CHAR(2),
    Preco_Unit_Peso DECIMAL(10, 2),
    Preco_Unit_Valor DECIMAL(10, 2),
    FOREIGN KEY (UF) REFERENCES Estado(UF)
);

-- Tabela FUNCIONARIO
CREATE TABLE Funcionario (
    Num_Reg INT PRIMARY KEY,
    Nome_Func VARCHAR(100)
);

-- Tabela CLIENTE
CREATE TABLE Cliente (
    Cod_Cli INT PRIMARY KEY,
    Data_Insc DATE,
    Endereco VARCHAR(200),
    Telefone VARCHAR(20),
    Tipo_Cliente VARCHAR(20) CHECK (Tipo_Cliente IN ('Pessoa Juridica', 'Pessoa Fisica'))
);

-- Tabela PESSOA JURIDICA
CREATE TABLE Pessoa_Juridica (
    Cod_Cli INT PRIMARY KEY,
    Razao_Social VARCHAR(100),
    Insc_Estadual VARCHAR(50),
    CNPJ VARCHAR(18),
    FOREIGN KEY (Cod_Cli) REFERENCES Cliente(Cod_Cli)
);

-- Tabela PESSOA FISICA
CREATE TABLE Pessoa_Fisica (
    Cod_Cli INT PRIMARY KEY,
    Nome_Cli VARCHAR(100),
    CPF VARCHAR(14),
    FOREIGN KEY (Cod_Cli) REFERENCES Cliente(Cod_Cli)
);

-- Tabela FRETE
CREATE TABLE Frete (
    Num_Conhec INT PRIMARY KEY,
    Peso DECIMAL(10, 2),
    Valor DECIMAL(10, 2),
    Pedagio DECIMAL(10, 2),
    ICMS DECIMAL(10, 2),
    Data_Frete DATE,
    Quem_Paga VARCHAR(50),
    Peso_Ou_Valor VARCHAR(50),
    Origem_CID INT,
    Destino_CID INT,
    Remetente_Cli INT,
    Destinatario_Cli INT,
    FOREIGN KEY (Origem_CID) REFERENCES Cidade(Codigo_CID),
    FOREIGN KEY (Destino_CID) REFERENCES Cidade(Codigo_CID),
    FOREIGN KEY (Remetente_Cli) REFERENCES Cliente(Cod_Cli),
    FOREIGN KEY (Destinatario_Cli) REFERENCES Cliente(Cod_Cli)
);

