import streamlit as st
from cliente import Cliente
from estado import Estado
from cidade import Cidade
from funcionario import Funcionario
from frete import Frete
from ligar_connect import connection
import pandas as pd

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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Cliente", "Estado", "Cidade", "Funcionário", "Frete", "B.I de Fretes", "Média de Fretes", "Funcionário - PJ"])

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

    # Seleção do cliente para edição
    dados_clientes = Cliente.obter_clientes()
    
    meus_clientes = list(zip(dados_clientes["cod_cli"], dados_clientes["tipo_cliente"], dados_clientes["data_insc"]))
    cliente_selecionado_edicao = st.selectbox(
        "Selecione o cliente para editar", 
        meus_clientes,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]} - {x[2]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário

    if cliente_selecionado_edicao:
        cod_cliente = cliente_selecionado_edicao[0]
        cliente_data_insc = cliente_selecionado_edicao[2]
        cliente_tipo_atual = cliente_selecionado_edicao[1]
        
        with st.form(key="edit_cliente"):
            st.title(f"Editar Cliente {cod_cliente}")
            st.write("Preencher Tabela Cliente")
            #input_cod_cliente =st.number_input(label="Insira o código do cliente", format="%d", step=1, value=cliente_selecionado_edicao[0]) 
            input_data_insc = st.date_input(label="Insira a data de INSC")
            input_endereco = st.text_input(label="Insira o endereço")
            input_telefone = st.number_input(label="Insira um telefone de contato", format="%s")
            input_tipo_cliente = st.selectbox("Selecione o tipo de cliente", ["Pessoa Fisica", "Pessoa Juridica"])
            
            input_cliente_button_submit = st.form_submit_button(label=f"Editar Cliente {cliente_selecionado_edicao[0]}")
            
            if input_cliente_button_submit:  #(Se o input_botton_submit for True = Apertado)
                cliente = Cliente(
                    cod_cliente=cod_cliente,
                    data_insc=input_data_insc,
                    endereco=input_endereco,
                    telefone=input_telefone,
                    tipo_cliente=input_tipo_cliente
                )
                cliente.editar_cliente()
                #ClienteController.Incluir(cliente)
                st.success(f'Cliente {cod_cliente} Editado com sucesso!', icon="✅")
                #print(type, input_data_insc) debugar isso pq tava dando erro dum caralho"""
            
    st.title("Excluir Cliente")
    # Seleção do cliente para exclusão
    dados_clientes = Cliente.obter_clientes()
    
    meus_clientes = list(zip(dados_clientes["cod_cli"], dados_clientes["tipo_cliente"], dados_clientes["data_insc"]))
    cliente_selecionado = st.selectbox(
        "Selecione o cliente para excluir", 
        meus_clientes,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]} - {x[2]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário
    
    # Botão para excluir cliente
    if st.button(f"Excluir cliente {cliente_selecionado[0]}"):
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

    # Seleção dos estados para edição
    dados_estados = Estado.obter_estados()
    
    meus_estados = dados_estados["uf"].tolist()
    estado_selecionado_edicao = st.selectbox(
        "Selecione o estado para editar", 
        meus_estados,  # Passa a lista de tuplas
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário

    if estado_selecionado_edicao:
        uf = estado_selecionado_edicao
        
        with st.form(key="edit_estado"):
            st.title(f"Editar Estado {uf}")
            st.write("Preencher Tabela Estado")
            #input_uf =st.selectbox("Selecione a unidade federativa", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
            input_icms_local = st.number_input(label="Insira o ICMS do estado", step=0.5, format="%.2f")
            input_nome_est = st.text_input(label="Insira o nome do estado")
            input_icms_outro_uf = st.number_input(label="Insira o ICMS do outro estado", step=0.5, format="%.2f")
           # input_estado_button_submit = st.form_submit_button(label="Mandar")
            input_estado_button_submit = st.form_submit_button(label=f"Editar Estado {uf}")
            
            if input_estado_button_submit:  #(Se o input_botton_submit for True = Apertado)
                    estado = Estado(
                        uf=uf,
                        icms_local=input_icms_local,
                        nome_est=input_nome_est,
                        icms_outro_uf=input_icms_outro_uf
                    )
                    estado.editar_estado()
                    #EstadoController.Incluir(estado)
                    st.success(f'Estado {uf} Editado com sucesso!', icon="✅")
                    #print(type, input_data_insc) debugar isso pq tava dando erro dum caralho
        
    # Seleção do cliente para exclusão
    dados_estados = Estado.obter_estados()
    
    meus_estados = list(zip(dados_estados["uf"], dados_estados["nome_est"]))
    estado_selecionado = st.selectbox(
        "Selecione o estado para excluir", 
        meus_estados,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário
    
    # Botão para excluir estado 
    if st.button(f"Excluir Estado {estado_selecionado[0]}"):
        if estado_selecionado:
            Estado.excluir_estado(estado_selecionado[0])  # Chama a função para excluir o estado
            #st.experimental_rerun()  # Atualiza a página para refletir a exclusão
            st.success(f"Estado {estado_selecionado[0]}{estado_selecionado[1]} excluído com sucesso!", icon="🤐")
        else:
            st.warning("Selecione um estado para excluir")
        
    
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
    
    #Seleção das cidades para edição
    dados_cidades = Cidade.obter_cidades()

    minhas_cidades = list(zip(dados_cidades["nome_cid"], dados_cidades["codigo_cid"]))
    cidade_selecionada_edicao = st.selectbox(
        "Selecione a cidade para editar",
        minhas_cidades,
        format_func=lambda x: f"{x[0]} - {x[1]}"
    )

    if cidade_selecionada_edicao:
        nome_cid = cidade_selecionada_edicao[0]
        codigo_cidade = cidade_selecionada_edicao[1]

        with st.form(key="edit_cidade"):
            st.title(f"Editar cidade {nome_cid}")
            st.write("Preencher Tabela Cidade")
            input_nome_cid = st.text_input(label="Insira o nome da cidade")
            input_preco_unit_valor = st.number_input(label="Insira o preco por unidade", step=0.5, format="%.2f")
            input_preco_unit_peso = st.number_input(label="Insira o preco por peso", step=0.5, format="%.2f")
            opcoes_estados = dados_estados["uf"].tolist()
            input_uf = st.selectbox(
            "Selecione a unidade federativa", 
            opcoes_estados
            )
            
            input_cidade_button_submit = st.form_submit_button(label=f"Editar cidade {nome_cid}")

            if input_cidade_button_submit:
                cidade = Cidade(
                    codigo_cid=codigo_cidade,
                    nome_cid=input_nome_cid,
                    preco_unit_valor=input_preco_unit_valor,
                    preco_unit_peso = input_preco_unit_peso,
                    uf=input_uf
                )
                cidade.editar_cidade()

                st.success(f"Cidade {nome_cid} editada com sucesso!", icon="✅")
    
    # Seleção do cliente para exclusão
    dados_cidades = Cidade.obter_cidades()
    
    meus_cidades = list(zip(dados_cidades["uf"], dados_cidades["nome_cid"], dados_cidades["codigo_cid"]))
    cidade_selecionado = st.selectbox(
        "Selecione a cidade para excluir", 
        meus_cidades,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário
    
    cidade = cidade_selecionado
    
    # Botão para excluir estado 
    if st.button(f"Excluir {cidade[1]}"):
        if cidade_selecionado:
            Cidade.excluir_cidade(cidade_selecionado[2])  # Chama a função para excluir a cidade
            #st.experimental_rerun()  # Atualiza a página para refletir a exclusão
            st.success(f"Cidade {cidade_selecionado[2]} - {cidade_selecionado[1]} excluído com sucesso!", icon="🤐")
        else:
            st.warning("Selecione uma cidade para excluir")
        

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
            
    # Seleção do funcioanrio para edição
    dados_funcionarios = Funcionario.obter_funcionarios()
    
    meus_funcionarios = list(zip(dados_funcionarios["num_reg"], dados_funcionarios["nome_func"]))
    funcionario_selecionado_edicao = st.selectbox(
        "Selecione o funcionário para editar", 
        meus_funcionarios,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário

    with st.form(key="edit_funcionario"):
            st.title(f"Editar Funcionário {funcionario_selecionado_edicao[0]}")
            st.write("Preencher Tabela Funcionário")
            
            #input_num_reg = st.number_input(label="Insira o número do funcionário", format="%d", value=funcionario_selecionado_edicao[0])
            input_nome_reg = st.text_input(label="Insira o nome do funcionário")
            
            input_funcionario_button_submit = st.form_submit_button(label=f"Editar Funcionário {funcionario_selecionado_edicao[0]}")
            
            input_num_reg = funcionario_selecionado_edicao[0]
            
            if input_funcionario_button_submit:  #(Se o input_botton_submit for True = Apertado)
                funcionario = Funcionario(
                    num_reg=input_num_reg,
                    nome_func=input_nome_reg
                )
                funcionario.editar_funcionario()
                
                st.success(f'Funcionário {input_num_reg} Editado com sucesso!', icon="✅")
        
    # Seleção do cliente para exclusão
    dados_funcionarios = Funcionario.obter_funcionarios()
    
    meus_funcionarios = list(zip(dados_funcionarios["num_reg"], dados_funcionarios["nome_func"]))
    funcionario_selecionado = st.selectbox(
        "Selecione o funcionário para excluir", 
        meus_funcionarios,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - {x[1]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário
    
    # Botão para excluir funcionário 
    if st.button("Excluir Funcionário"):
        if funcionario_selecionado:
            Funcionario.excluir_funcionario(funcionario_selecionado[0])  # Chama a função para excluir o funcionário
            #st.experimental_rerun()  # Atualiza a página para refletir a exclusão
            st.success(f"Funcionário {funcionario_selecionado[0]} excluído com sucesso!", icon="🤐")
        else:
            st.warning("Selecione um funcionário para excluir")
        
    
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
        
        dados_funcionarios = Funcionario.obter_funcionarios()
        
        opcoes_funcionarios = list(zip(dados_funcionarios["num_reg"], dados_funcionarios["nome_func"]))
        
        funcionario_escolhido = st.selectbox(
            "Selecione o funcionário que está em atendimento",
            opcoes_funcionarios, 
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )
        input_funcionario = funcionario_escolhido[0] # Vamos pegar o código do funcionário pois coloquei na tabela como INT a coluna funcionario
        
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
                funcionario=input_funcionario,
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


    # Seleção do cliente para edição
    dados_fretes = Frete.obter_fretes()
    
    meus_fretes = list(zip(
        dados_fretes["num_conhec"],
        dados_fretes["peso"],
        dados_fretes["valor"],
        dados_fretes["pedagio"],
        dados_fretes["icms"],
        dados_fretes["data_frete"],
        dados_fretes["quem_paga"],
        dados_fretes["funcionario"],
        dados_fretes["peso_ou_valor"],
        dados_fretes["origem_cid"],
        dados_fretes["destino_cid"],
        dados_fretes["remetente_cli"],
        dados_fretes["destinatario_cli"],
    ))
    frete_selecionado_edicao = st.selectbox(
        "Selecione o frete para editar", 
        meus_fretes,  # Passa a lista de tuplas
        format_func=lambda x: f"{x[0]} - Valor R$ {x[1]}" 
        )  # Exemplo para pegar a primeira coluna, ajuste conforme necessário

    if frete_selecionado_edicao:
        num_conhec = frete_selecionado_edicao[0]
        peso = frete_selecionado_edicao[1]
        valor = frete_selecionado_edicao[2]
        pedagio =frete_selecionado_edicao[3]
        icms =frete_selecionado_edicao[4]
        data_frete =frete_selecionado_edicao[5]
        quem_paga =frete_selecionado_edicao[6]
        funcionario =frete_selecionado_edicao[7]
        peso_ou_valor =frete_selecionado_edicao[8]
        origem_cid =frete_selecionado_edicao[9]
        destino_cid =frete_selecionado_edicao[10]
        remetente_cli =frete_selecionado_edicao[11]
        destinatario_cli =frete_selecionado_edicao[12]
        
        with st.form(key="edit_frete"):
            st.title(f"Editar Frete {num_conhec}")
            st.write("Preencher Tabela Frete")
           
            #input_numero_conhecimento = st.number_input(label="Insira o Numero de conhecimento do frete", format="%s")
            input_peso_frete = st.number_input(label="Insira o peso do Frete")
            input_valor = st.number_input(label="Insira o valor do Frete")
            input_pedagio = st.text_input(label="Insira o valor do Pedagio do Frete")
            input_icms_frete = st.number_input(label="Insira o icms do Frete")
            input_data_frete = st.date_input(label="Insira a data do Frete")
            input_nome_quem_vai_pagar = st.text_input(label="Insira o nome de quem vai pagar o Frete")
            
            dados_funcionarios = Funcionario.obter_funcionarios()
        
            opcoes_funcionarios = list(zip(dados_funcionarios["num_reg"], dados_funcionarios["nome_func"]))
            
            funcionario_escolhido = st.selectbox(
                "Selecione o funcionário que está em atendimento",
                opcoes_funcionarios, 
                format_func=lambda x: f"{x[0]} - {x[1]}"
            )
            input_funcionario = funcionario_escolhido[0] # Vamos pegar o código do funcionário pois coloquei na tabela como INT a coluna funcionario
            
            
            # input_peso_ou_valor = st.text_input(label="Insira se vai ser peso ou valor o Frete")

            input_peso_ou_valor = st.radio(
            "Escolha o metodo de calculo do frete :point_down:",
            ["peso", "valor"],
            key="peso_valor",
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
            
            input_cliente_button_submit = st.form_submit_button(label=f"Editar Frete {frete_selecionado_edicao[0]}")
                
            if input_cliente_button_submit:  #(Se o input_botton_submit for True = Apertado)
                frete = Frete(
                        num_conhec=input_numero_conhecimento,
                        peso=input_peso_frete,
                        valor=input_valor,
                        pedagio=input_pedagio,
                        icms=input_icms_frete,
                        data_frete=input_data_frete,
                        quem_paga=input_nome_quem_vai_pagar,
                        funcionario=input_funcionario,
                        peso_ou_valor=input_peso_ou_valor,
                        origem_cid=cidade_origem_selecionada,
                        destino_cid=input_cidade_destino,
                        remetente_cli=input_remetente_frete,
                        destinatario_cli=input_destinatario
                        )
                frete.editar_frete()
                #ClienteController.Incluir(cliente)
                st.success(f'Frete {num_conhec} Editado com sucesso!', icon="✅")
                #print(type, input_data_insc) debugar isso pq tava dando erro dum caralho"""
                print("Origem CID:", cidade_origem_selecionada)
                print("Destino CID:", input_cidade_destino)


    dados_fretes = Frete.obter_fretes()

    meus_fretes = list(zip(dados_fretes["num_conhec"], dados_fretes["remetente_cli"], dados_fretes["destinatario_cli"], dados_fretes["quem_paga"]))
    frete_selecionado = st.selectbox(
        "Selecione o frete para excluir",
        meus_fretes, 
        format_func=lambda x: f"{x[0]} - {x[1]} - {x[2]} - {x[3]}"
    )

    if st.button(f"Excluir Frete {input_numero_conhecimento}"):
        if frete_selecionado:
            Frete.excluir_fretes(frete_selecionado[0])  # Chama a função para excluir o estado
            #st.experimental_rerun()  # Atualiza a página para refletir a exclusão
            st.success(f"Frete {input_numero_conhecimento} excluído com sucesso!", icon="🤐")
        else:
            st.warning("Selecione um frete para excluir")

with tab6:
    st.title("Arrecadações de Fretes")

    with st.form(key="include_arrecadaFrete"):
        st.write("Arrecadação de Frete por Estado/Cidade")

        # Dados de Estados e Cidades
        dados_cidades = Cidade.obter_cidades()
        
        #st.write(dados_cidades) #Ja começa debugando o fdp
        
        
        # Ajuste baseado no formato
        minhas_cidades = list(zip(dados_cidades["uf"], dados_cidades["nome_cid"]))  
        
        # Selecionar Estado e Cidade
        cidade_estado_selecionado = st.selectbox(
            "Selecione o Estado/Cidade",
            minhas_cidades,
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )

        submit_button = st.form_submit_button(f"Arrecadações de {cidade_estado_selecionado[0]} - {cidade_estado_selecionado[1]}")
        
        if submit_button:
            estado, cidade = cidade_estado_selecionado
            arrecadacao = Frete.obter_arrecadacao_por_cidade_estado(estado, cidade)
            
            if arrecadacao:
                st.markdown("***Resultados:***")
                for item in arrecadacao:
                    st.markdown(f"### {item['cidade_destino']} - {item['uf_destino']}")
                    st.markdown(f"- **Quantidade de Fretes**: {item['quantidade_fretes']}")
                    st.markdown(f"- **Valor Total Arrecadado**: R${item['total_arrecadado']:,.2f}")
                    #Back p debugar X(
                    print(f" {item['cidade_destino']} - {item['uf_destino']}")
                    print(f"- Quantidade de Fretes: {item['quantidade_fretes']}")
                    print(f"- Valor Total Arrecadado: R${item['total_arrecadado']:,.2f}")

            else:
                st.warning("Nenhum resultado encontrado para a consulta.")
                
with tab7:
    st.title("Média de Fretes por Estado")

    # Interface do usuário para selecionar o estado
    with st.form(key="form_frete"):
        st.write("Selecione o estado para visualizar as médias de fretes")

        # Obter os estados disponíveis no banco de dados
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT UF FROM Cidade;")
            estados_disponiveis = [row[0] for row in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            st.error(f"Erro ao obter os estados: {e}")
            estados_disponiveis = []

        # Dropdown para selecionar o estado
        estado_selecionado = st.selectbox("Selecione o Estado", estados_disponiveis)

        # Botão para submeter o formulário
        submit_button = st.form_submit_button("Calcular")

        if submit_button and estado_selecionado:
            # Chama o método da classe Frete para obter as médias
            media_fretes = Frete.obter_media_fretes_por_cidade_estado(estado_selecionado)

            if media_fretes:
                st.markdown("### Resultados:")
                for frete in media_fretes:
                    st.markdown(f"**Cidade:** {frete['cidade']}")
                    st.markdown(f"- **Média de Fretes de Origem:** {frete['media_fretes_origem']:.2f}")
                    st.markdown(f"- **Média de Fretes de Destino:** {frete['media_fretes_destino']:.2f}")
                    st.markdown("---")
            else:
                st.warning("Nenhum dado encontrado para o estado selecionado.")

with tab8:
    st.title("PJ´s Atendidos por Funcionários")

    with st.form(key="include_FuncionarioPJ"):
        st.write("Consulta de Fretes Realizados por Funcionários para Pessoas Jurídicas")

        # Entrada para Mês e Ano
        mes_ano = st.text_input("Informe o mês/ano (formato MM/AAAA):", placeholder="Ex: 01/2024")
        
        submit_button = st.form_submit_button("Consultar Fretes")
        
        if submit_button:
            # Verifica se a entrada é válida
            if "/" in mes_ano:
                try:
                    mes, ano = map(int, mes_ano.split('/'))  # Converte para inteiros
                    
                    # Busca os fretes pelo método na classe Frete
                    fretes = Frete.obter_fretes_funcionarios_pj(mes_ano)
                    
                    if fretes:
                        st.markdown("### Resultados:")
                        for frete in fretes:
                            st.markdown(f"**Número do Conhecimento:** {frete['num_conhecimento']}")
                            st.markdown(f"- **Data do Frete:** {frete['data_frete']}")
                            st.markdown(f"- **Representante Empresa (PJ):** {frete['representante_empresa']}")
                            st.markdown(f"- **Funcionário Responsável:** {frete['funcionario_responsavel']}")
                            st.markdown("---")
                    
                    else:
                        st.warning("Nenhum frete encontrado para o mês/ano informado.")

                except ValueError:
                    st.error("Erro ao processar o mês/ano. Certifique-se de usar o formato MM/AAAA e valores válidos.")
            else:
                st.error("Por favor, informe o mês/ano no formato MM/AAAA.")
