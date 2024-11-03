import streamlit as st
from cliente import Cliente

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

        

with tab2:
    st.title("CRUD ESTADO")
    ## FAZER A PARTE DO ESTADO AQUI
    
with tab3:
    st.title("CRUD CIDADE")
    ## FAZER A PARTE DO CIDADE AQUI
    
with tab4:
    st.title("CRUD FUNCIONÁRIO")
    ## FAZER A PARTE DO FUNCIONÁRIO AQUI
    
with tab5:
    st.title("CRUD FRETE")
    ## FAZER A PARTE DO FUNCIONÁRIO AQUI