import customtkinter as ctk


class ContainerSuperior(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=1000, height=130, bg_color="#98FB98",
                         fg_color="#98FB98", corner_radius=0, **kwargs)
        
        self.place(x=0, y=0)
        
        self.titulo = ctk.CTkLabel(
            self, 
            text="Mundo do Autônomo!", 
            font=("Arial", 32, "bold"), 
            text_color="#1A1A1A"
        )
    
        self.titulo.place(relx=0.5, rely=0.5, anchor="center")


class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=180, height=620, bg_color="#7CCD7C",
                         fg_color="#7CCD7C", corner_radius=0, **kwargs) 
        
        self.place(x=0, y=130)
        self.grid_propagate(False)
        
        
        self.cliente = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="CAD. CLIENTES", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_clientes 
        )     
        self.cliente.grid(row=0, column=0, pady=2) 

        
        self.produtos = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="CAD. PRODUTOS", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_produtos 
        )
        self.produtos.grid(row=1, column=0, pady=2)
        
        self.servicos = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="CAD. SERVIÇOS", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_servicos 
        )
        self.servicos.grid(row=2, column=0, pady=2)

        self.estoque = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="ESTOQUE", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_estoque 
        )
        self.estoque.grid(row=3, column=0, pady=2)

        self.orcamento = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="ORÇAMENTO", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_orcamento 
        )     
        self.orcamento.grid(row=4, column=0, pady=2) 

        
        self.os = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="ORDEM DE SERVIÇO", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_os 
        )
        self.os.grid(row=5, column=0, pady=2)
        
        self.pagamento = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="PAGAMENTOS", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_contas_pagar 
        )
        self.pagamento.grid(row=6, column=0, pady=2)

        self.recebimentos = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="RECEBIMENTOS", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_contas_receber 
        )
        self.recebimentos.grid(row=7, column=0, pady=2)

        self.abrir_caixa = ctk.CTkButton(
            self, 
            width=180, 
            height=40,
            fg_color="#2E8B57", 
            text="CAIXA", 
            font=("Century Gothic bold", 12), 
            corner_radius=0, 
            command=self.abrir_caixa 
        )
        self.abrir_caixa.grid(row=8, column=0, pady=2)

    def abrir_clientes(self):
        print("Botão de cadastro de clientes acionado!")

    def abrir_produtos(self):
        print("Botão de cadastro de produtos acionado!")

    def abrir_servicos(self):
        print("Botão de cadastro de serviços acionado!")

    def abrir_estoque(self):
        print("Botão estoque acionado!")   
        
    def abrir_orcamento(self):
        print("Botão orçamento acionado!")

    def abrir_os(self):
        print("Botão de ordem de serviço acionado!")

    def abrir_contas_pagar(self):
        print("Botão contas a pagar acionado!")

    def abrir_contas_receber(self):
        print("Botão conta a receber acionado!")   
        
    def abrir_caixa(self):
        print("Botão controle de caixa acionado!")


class Interface(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=820, height=620,
                          fg_color="white", corner_radius=0, **kwargs) 
        self.place(x=180, y=130)
