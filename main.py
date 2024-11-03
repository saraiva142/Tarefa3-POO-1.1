import streamlit as st
from cliente import Cliente
from estado import Estado
from cidade import Cidade

# Configurando o tema padrão
st.set_page_config(
    page_title="Tarefa3POO",
    page_icon=":blossom:",
    layout="wide",  # wide ou "centered"
)

st.title('Tarefa 3 - POO Em Banco de Dados :game_die:')
st.write('Alunos: João Saraiva - Walison Matheus - Arthur Rodrigues - Rodrigo Barros')
st.write('Professor: Joriver')

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Cliente", "Estado", "Cidade", "Funcionário", "Frete"])

with tab1:
    with st.form(key="include_cliente"):
        st.title("CRUD Cliente")
        st.write("Preencher Tabela Cliente")
        input_cod_cliente =st.number_input(label="Insira o código do cliente", format="%d", step=1) 
        input_data_insc = st.date_input(label="Insira a data de INSC")
        input_endereco = st.text_input(label="Insira o endereço")
        input_telefone = st.number_input(label="Insira um telefone de contato", format="%s")
        input_tipo_cliente = st.selectbox("Selecione o tipo de cliente", ["Pessoa Fisica", "Pessoa Juridica"])
        input_cliente_button_submit = st.form_submit_button(label="Enviar")
        

        if input_cliente_button_submit:  #(Se o input_botton_submit for True = Apertado)
            cliente = Cliente(
                cod_cliente=input_cod_cliente,
                data_insc=input_data_insc,
                endereco=input_endereco,
                telefone=input_telefone,
                tipo_cliente=input_tipo_cliente
            )
            cliente.inserir_cliente()
            #ClienteController.Incluir(cliente)
            st.success('Cadastrado com sucesso!', icon="✅")
            
            # Armazenando a instância do cliente no session_state
            st.session_state.cliente = cliente
    #else:
    #    st.error("É preciso preencher todos os campos")
    # Formulário para inserir dados adicionais da Pessoa Física ou Jurídica
    with st.form(key="include_pessoa"):
        st.write("Preencher Tabela Pessoa")
        # Reutilizar o cod_cliente para referenciar o cliente cadastrado
        input_cod_cliente_pessoa = st.number_input("Código do Cliente (deve ser o mesmo cadastrado)", value=input_cod_cliente, format="%d", step=1)
                
        if input_tipo_cliente == "Pessoa Fisica":
            input_nome_cli = st.text_input("Nome Completo")
            input_cpf = st.text_input("CPF")
        elif input_tipo_cliente == "Pessoa Juridica":
            input_razao_social = st.text_input("Razão Social")
            input_insc_estadual = st.text_input("Inscrição Estadual")
            input_cnpj = st.text_input("CNPJ")
                
        input_pessoa_button_submit = st.form_submit_button(label="Enviar")

        if input_pessoa_button_submit:
            # Acessando a instância do cliente do session_state
            cliente = st.session_state.get("cliente")
            if cliente:  # Verifica se o cliente foi cadastrado anteriormente
                if input_tipo_cliente == "Pessoa Fisica":
                    cliente.inserir_pessoa_fisica(nome=input_nome_cli, cpf=input_cpf)
                    st.success("Pessoa Física cadastrada com sucesso!", icon="✅")
                elif input_tipo_cliente == "Pessoa Juridica":
                    cliente.inserir_pessoa_juridica(razao_social=input_razao_social, insc_estadual=input_insc_estadual, cnpj=input_cnpj)
                    st.success("Pessoa Jurídica cadastrada com sucesso!", icon="✅")
        
        # Visualização de dados da tabela Cliente
    st.subheader("Visualizar Clientes Cadastrados")
    if st.button("Atualizar Dados"):
        dados_clientes = Cliente.obter_clientes()
        if not dados_clientes.empty:
            st.dataframe(dados_clientes)
        else:
            st.write("Nenhum cliente encontrado na tabela.")

        

with tab2:
    with st.form(key="include_estado"):
        st.write("Preencher Tabela Estado")
        input_uf = st.selectbox("Selecione a unidade federativa", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        input_icms_local = st.number_input(label="Insira o ICMS do estado", step=0.5, format="%.2f")
        input_nome_est = st.text_input(label="Insira o nome do estado")
        input_icms_outro_uf = st.number_input(label="Insira o ICMS do outro estado", step=0.5, format="%.2f")
        input_estado_button_submit = st.form_submit_button(label="Enviar")
        

        if input_estado_button_submit:  #(Se o input_botton_submit for True = Apertado)
            estado = Estado(
                uf=input_uf,
                icms_local=input_icms_local,
                nome_est=input_nome_est,
                icms_outro_uf=input_icms_outro_uf
            )
            estado.inserir_estado()
            #ClienteController.Incluir(cliente)
            st.success('Cadastrado com sucesso!', icon="✅")
            
            # Armazenando a instância do cliente no session_state
            st.session_state.estado = estado
    #else:
    #    st.error("É preciso preencher todos os campos")
    # Visualização de dados da tabela Estado
    st.subheader("Visualizar Estados Cadastrados")
    if st.button("Atualizar Dados Estados"):
        dados_estados = Estado.obter_estados()
        if not dados_estados.empty:
            st.dataframe(dados_estados)
        else:
            st.write("Nenhum estado encontrado na tabela.")
    
    
with tab3:
    st.title("CRUD CIDADE")
    with st.form(key="include_cidade"):
        st.write("Preencher Tabela Cidade")
        input_nome_cid = st.text_input(label="Insira o nome da cidade")
        input_codigo_cid = st.text_input(label="Insira o codigo da cidade")
        input_preco_unit_valor = st.number_input(label="Insira o preco por unidade", step=0.5, format="%.2f")
        input_preco_unit_peso = st.number_input(label="Insira o preco por peso", step=0.5, format="%.2f")
        input_uf = st.selectbox("Selecione a unidade federativa", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        input_cidade_button_submit = st.form_submit_button(label="Enviar")

        if input_cidade_button_submit:  #(Se o input_botton_submit for True = Apertado)
            cidade = Cidade(
                nome_cid=input_nome_cid,
                codigo_cid=input_codigo_cid,
                preco_unit_valor=input_preco_unit_valor,
                preco_unit_peso = input_preco_unit_peso,
                uf=input_uf
                
            )
            cidade.inserir_cidade()
            #ClienteController.Incluir(cliente)
            st.success('Cidade Cadastrada com sucesso!', icon="✅")
            
            # Armazenando a instância do cliente no session_state
            st.session_state.cidade = cidade
            
    # Visualização de dados da tabela Cidade
    st.subheader("Visualizar Cidades Cadastrados")
    if st.button("Atualizar Dados Cidades"):
        dados_cidades = Cidade.obter_cidades()
        if not dados_cidades.empty:
            st.dataframe(dados_cidades)
        else:
            st.write("Nenhuma cidade encontrado na tabela.")
    
with tab4:
    st.title("CRUD FUNCIONÁRIO")
    ## FAZER A PARTE DO FUNCIONÁRIO AQUI
    
with tab5:
    st.title("CRUD FRETE")
    ## FAZER A PARTE DO FUNCIONÁRIO AQUI