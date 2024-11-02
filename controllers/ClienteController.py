class ClienteController:
    def criar

       cliente = Cliente(
            cod_cliente=input_cod_cliente,
            data_insc=input_data_insc,
            endereco=input_endereco,
            telefone=input_telefone,
            tipo_cliente=input_tipo_cliente
        )
        cliente.inserir_cliente()


    def editar