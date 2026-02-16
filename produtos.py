import customtkinter as ctk # Importa a biblioteca para criar os componentes visuais

# --- CLASSE PARA CADASTRO DE PRODUTOS ---
class Produtos(ctk.CTkFrame): # Herda de CTkFrame para ser uma tela acoplável
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) # Inicializa o frame na interface central
        self.inputs = {} # Dicionário para armazenar as referências dos campos

    def abrir_produtos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1) # Faz a tela preencher o espaço da interface
        self.configure(fg_color="white") # Define o fundo da tela como branco

        # Lista de campos: (Rótulo, Chave interna, Mensagem de orientação)
        campos = [
            ("Produto:", "produto", "Nome do item..."),
            ("Marca:", "marca", "Fabricante ou marca..."),
            ("Valor Compra:", "v_compra", "R$ 0,00"),
            ("Valor Venda:", "v_venda", "R$ 0,00"),
            ("Quantidade:", "quantidade", "Ex: 10")
        ]

        # Loop para construir a interface de produtos automaticamente
        for i, (txt, chave, msg) in enumerate(campos):
            # Cria o rótulo verde escuro
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")

            # Cria o campo de entrada com a identidade visual padronizada
            entry = ctk.CTkEntry(
                self, 
                width=400, 
                height=40, 
                font=("Arial", 16, "bold"),
                placeholder_text=msg,
                fg_color="#F0F0F0", # Fundo cinza claro
                bg_color="white",   # Fundo externo branco
                border_width=0,     # Sem bordas laterais
                corner_radius=50,   # Totalmente arredondado
                text_color="black"
            )
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = entry # Guarda a referência para coletar os dados depois

# --- CLASSE PARA CADASTRO DE SERVIÇOS ---
class Servicos(ctk.CTkFrame): # Também herda de CTkFrame
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}

    def abrir_servicos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        # Campos específicos para serviços
        campos_serv = [
            ("Descrição:", "descricao", "Ex: Manutenção de Ar Condicionado..."),
            ("Valor Custo:", "v_custo", "Custos operacionais..."),
            ("Valor Venda:", "v_venda", "Preço final do serviço...")
        ]

        # Loop para construir a interface de serviços
        for i, (txt, chave, msg) in enumerate(campos_serv):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")

            entry = ctk.CTkEntry(
                self, 
                width=400, 
                height=40, 
                font=("Arial", 16, "bold"),
                placeholder_text=msg,
                fg_color="#F0F0F0", # Fundo cinza claro
                bg_color="white",   # Fundo externo branco
                border_width=0,     # Sem bordas
                corner_radius=50,   # Arredondado
                text_color="black"
            )
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = entry 
