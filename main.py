import streamlit as st
from cliente import Cliente
from estado import Estado
from cidade import Cidade
from funcionario import Funcionario
from frete import Frete

# Configurando o tema padrão
st.set_page_config(
    page_title="Tarefa3POO",
    page_icon=":blossom:",
    layout="wide",  # wide ou "centered"
)

st.title('Tarefa 3 - POO Em Banco de Dados :game_die:')
st.write('Alunos: João Saraiva - Walison Matheus - Arthur Rodrigues - Rodrigo Barros')
st.write('Professor: Joriver')

url = "https://github.com/saraiva142/Tarefa3-POO-1.1"

st.markdown("[Código fonte GitHub](%s)" % url)

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
    if st.button("Visualizar Dados"):
        dados_clientes = Cliente.obter_clientes()
          
        if not dados_clientes.empty:
            st.dataframe(dados_clientes)

            #Cliente.exibir_tabela(dados_clientes)
        else:
            st.write("Nenhum cliente encontrado na tabela.")
        
    # Filtro para visualizar Pessoas Físicas ou Jurídicas
    st.subheader("Visualizar Pessoas")
    tipo_cliente = st.selectbox("Selecione o tipo de cliente para visualização", ["Pessoa Física", "Pessoa Jurídica"])

    if st.button("Visualizar Dados de Pessoas"):
        if tipo_cliente == "Pessoa Física":
            dados_pessoas_fisicas = Cliente.obter_pessoas_fisicas()
            if not dados_pessoas_fisicas.empty:
                st.dataframe(dados_pessoas_fisicas)
            else:
                st.write("Nenhum registro encontrado para pessoas físicas.")
        elif tipo_cliente == "Pessoa Jurídica":
            dados_pessoas_juridicas = Cliente.obter_pessoas_juridicas()
            if not dados_pessoas_juridicas.empty:
                st.dataframe(dados_pessoas_juridicas)
            else:
                st.write("Nenhum registro encontrado para pessoas jurídicas.")
    
    # Seleção do cliente para exclusão
    dados_clientes = Cliente.obter_clientes()
    
    meus_clientes = list(zip(dados_clientes["cod_cli"], dados_clientes["tipo_cliente"], dados_clientes["data_insc"]))
    cliente_selecionado = st.selectbox(
        "Selecione o cliente para excluir", 
        meus_clientes,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]} - {x[2]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário
    
    # Botão para excluir cliente
    if st.button("Excluir cliente"):
        if cliente_selecionado:
            Cliente.excluir_cliente(cliente_selecionado[0])  # Chama a função para excluir o cliente
            #st.experimental_rerun()  # Atualiza a página para refletir a exclusão
            st.success(f"Cliente {cliente_selecionado[0]} excluído com sucesso!", icon="🤐")
        else:
            st.warning("Selecione um cliente para excluir")
        

with tab2:
    with st.form(key="include_estado"):
        st.title("CRUD Estado")
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
    if st.button("Visualizar Dados Estados"):
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
        
        #input_uf = st.selectbox("Selecione a unidade federativa", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        dados_estados = Estado.obter_estados()

        # opcoes_cidades = [(cidade.codigo_cid, cidade.nome_cid) for cidade in dados_cidades]

        opcoes_estados = dados_estados["uf"].tolist()
        
        input_uf = st.selectbox(
          "Selecione a unidade federativa", 
          opcoes_estados
        )
        
        
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
    if st.button("Visualizar Dados Cidades"):
        dados_cidades = Cidade.obter_cidades()
        if not dados_cidades.empty:
            st.dataframe(dados_cidades)
        else:
            st.write("Nenhuma cidade encontrado na tabela.")
    
with tab4:
    st.title("CRUD FUNCIONÁRIO")
    ## FAZER A PARTE DO FUNCIONÁRIO AQUI
    with st.form(key="include_funcionario"):
        st.write("Preencher Tabela Funcionario")
        input_numero_funcionario = st.number_input(label="Insira o número do funcionário", format="%s")
        input_nome_funcionario = st.text_input(label="Insira o nome do Funcionário")
        input_funcionario_button_submit = st.form_submit_button(label="Enviar")
        

        if input_funcionario_button_submit:  #(Se o input_botton_submit for True = Apertado)
            funcionario = Funcionario(
                num_reg=input_numero_funcionario,
                nome_func=input_nome_funcionario
            )
            funcionario.inserir_funcionario()
            #ClienteController.Incluir(cliente)
            st.success('Funcionário Cadastrado com sucesso!', icon="✅")
    #else:
    #    st.error("É preciso preencher todos os campos")
    # Visualização de dados da tabela Estado
    st.subheader("Visualizar Funcionários Cadastrados")
    if st.button("Atualizar Dados Funcionários"):
        dados_funcionarios = Funcionario.obter_funcionarios()
        if not dados_funcionarios.empty:
            st.dataframe(dados_funcionarios)
        else:
            st.write("Nenhum estado encontrado na tabela.")
    
with tab5:
    st.title("CRUD FRETE")
    
    with st.form(key="include_frete"):
        st.write("Preencher Tabela Frete")
        input_numero_conhecimento = st.number_input(label="Insira o Numero de conhecimento do frete", format="%s")
        input_peso_frete = st.number_input(label="Insira o peso do Frete")
        input_valor = st.number_input(label="Insira o valor do Frete")
        input_pedagio = st.text_input(label="Insira o valor do Pedagio do Frete")
        input_icms_frete = st.number_input(label="Insira o icms do Frete")
        input_data_frete = st.date_input(label="Insira a data do Frete")
        input_nome_quem_vai_pagar = st.text_input(label="Insira o nome de quem vai pagar o Frete")
        
        # input_peso_ou_valor = st.text_input(label="Insira se vai ser peso ou valor o Frete")

        input_peso_ou_valor = st.radio(
          "Escolha o metodo de calculo do frete :point_down:",
          ["peso", "valor"],
          key="choise",
        )
  
        # input_cidade_origem = st.text_input(label="Insira a cidade de origem do Frete")
        dados_cidades = Cidade.obter_cidades()

        # opcoes_cidades = [(cidade.codigo_cid, cidade.nome_cid) for cidade in dados_cidades]

        opcoes_cidades = list(zip(dados_cidades["codigo_cid"], dados_cidades["nome_cid"]))
        
        codigo_cidade_origem = st.selectbox(
          "Selecione a cidade de origem", 
          opcoes_cidades, 
          format_func=lambda x: x[1]
        )
        # Armazenando o código da cidade de origem
        cidade_origem_selecionada = codigo_cidade_origem[0]
        #Debugar: print(f'Cidade: {cidade_origem_selecionada}')

        # cidade_origem_selecionada = st.text_input(label="Insira a cidade de origem do Frete")
        #input_cidade_destino = st.text_input(label="Insira a cidade de destino do Frete")

        codigo_cidade_destino = st.selectbox(
          "Selecione a cidade de destino", 
          opcoes_cidades, 
          format_func=lambda x: x[1]
        )
        # Armazenando o código da cidade de origem
        input_cidade_destino = codigo_cidade_destino[0]
        # Debugar: print(f'Cidade: {input_cidade_destino}')
        
        
        #input_remetente_frete = st.text_input(label="Insira o remetente do Frete")
        
        dados_clientes = Cliente.obter_clientes()

        opcoes_clientes = dados_clientes["cod_cli"].tolist()
        
        input_remetente_frete = st.selectbox(
          "Selecione o código do remetente", 
          opcoes_clientes
        )
        #input_destinatario = st.text_input(label="Insira o destinatario do Frete")
        input_destinatario = st.selectbox(
            "Selecione o código do destinatário",
            opcoes_clientes
        )
        input_frete_button_submit = st.form_submit_button(label="Enviar")
        
        if input_frete_button_submit:  #(Se o input_botton_submit for True = Apertado)
            frete = Frete(
                num_conhec=input_numero_conhecimento,
                peso=input_peso_frete,
                valor=input_valor,
                pedagio=input_pedagio,
                icms=input_icms_frete,
                data_frete=input_data_frete,
                quem_paga=input_nome_quem_vai_pagar,
                peso_ou_valor=input_peso_ou_valor,
                origem_cid=cidade_origem_selecionada,
                destino_cid=input_cidade_destino,
                remetente_cli=input_remetente_frete,
                destinatario_cli=input_destinatario,
            )
            frete.inserir_frete()
            #ClienteController.Incluir(cliente)
            st.success('Frete Cadastrado com sucesso!', icon="✅")
        st.subheader("Visualizar Fretes Cadastrados")
    if st.button("Visualizar Dados Fretes"):
        dados_fretes = Frete.obter_fretes()
        if not dados_fretes.empty:
            st.dataframe(dados_fretes)
        else:
            st.write("Nenhum frete encontrado na tabela.")
    ## FAZER A PARTE DO FUNCIONÁRIO AQUI