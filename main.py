import streamlit as st
from funcoes import inserir_cliente

# Configurando o tema padrão
st.set_page_config(
    page_title="Tarefa3POO",
    page_icon=":blossom:",
    layout="wide",  # wide ou "centered"
)

st.title('Tarefa 3 - POO Em Banco de Dados :game_die:')
st.write('Alunos: João Saraiva - Walison Matheus - Arthur Rodrigues - Rodrigo Barros')
st.write('Professor: Joriver')

with st.form(key="include_cliente"):
    st.write("Preencher Tabela Cliente")
    input_cod_cliente =st.number_input(label="Insira o código do cliente", format="%d", step=1) 
    input_data_insc = st.date_input(label="Insira a data de INSC")
    input_endereco = st.text_input(label="Insira o endereço")
    input_telefone = st.number_input(label="Insira um telefone de contato", format="%s")
    input_tipo_cliente = st.selectbox("Selecione o tipo de cliente", ["Pessoa Fisica", "Pessoa Juridica"])
    input_cliente_button_submit = st.form_submit_button(label="Enviar")
    

    if input_cliente_button_submit:  #(Se o input_botton_submit for True = Apertado)
        inserir_cliente(input_cod_cliente, input_data_insc, input_endereco, input_telefone, input_tipo_cliente)
        #ClienteController.Incluir(cliente)
        st.success('Cadastrado com sucesso!', icon="✅")
#else:
#    st.error("É preciso preencher todos os campos")