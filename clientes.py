import customtkinter as ctk # Importa a biblioteca para criar a interface moderna

# --- CLASSE PARA CADASTRO DE PESSOA FÍSICA ---
class PessoaFisica(ctk.CTkFrame): # Cria a classe herdando de CTkFrame (funciona como uma tela container)
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) # Inicializa o frame dentro da janela principal (master)
        self.inputs = {} # Cria um dicionário vazio para armazenar as referências de cada campo de texto

    def abrir_fisica(self):
        self.place(x=0, y=0, relwidth=1, relheight=1) # Posiciona o frame preenchendo toda a área disponível
        self.configure(fg_color="white") # Define a cor de fundo desta tela como branco

        # Lista de Tuplas: Cada item contém (Texto do Label, Nome da Chave, Texto de Orientação)
        campos_pf = [
            ("Nome do Cliente:", "nome", "Digite o nome completo..."),
            ("CPF:", "cpf", "000.000.000-00"), 
            ("Endereço:", "logradouro", "Rua, Avenida, Logradouro..."),
            ("Número:", "numero", "Nº"),
            ("Bairro:", "bairro", "Digite o bairro..."),
            ("Cidade:", "cidade", "Sua cidade..."),
            ("Estado:", "estado", "UF"),
            ("CEP:", "cep", "00000-000"),
            ("Telefone:", "telefone", "(00) 00000-0000"),
            ("Email:", "email", "exemplo@email.com")
        ]

        # Loop 'for' que percorre a lista para criar automaticamente os labels e campos
        for i, (txt, chave, msg) in enumerate(campos_pf):
            # Cria o texto descritivo (Label)
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w") # Posiciona à esquerda (w)

            # Cria a caixa de entrada de texto (Entry)
            entry = ctk.CTkEntry(
                self, width=400, height=40, font=("Arial", 16, "bold"),
                placeholder_text=msg, # Define o texto que some ao digitar
                fg_color="#F0F0F0", bg_color="white", border_width=0,
                corner_radius=50, text_color="black" # Estilo arredondado e sem borda
            )
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w") # Posiciona ao lado do label
            self.inputs[chave] = entry # Guarda o objeto do campo no dicionário usando a 'chave'

        # Cria o botão de ação para salvar
        self.btn_salvar = ctk.CTkButton(
            self, text="SALVAR CLIENTE", fg_color="#2E8B57", hover_color="#145B06",
            font=("Arial", 14, "bold"), corner_radius=50, command=self.salvar_pf
        )
        # Posiciona o botão abaixo do último campo criado (row=len)
        self.btn_salvar.grid(row=len(campos_pf), column=1, pady=20, sticky="e", padx=5)

    def salvar_pf(self):
        # Captura o texto de cada campo e organiza em um novo dicionário de dados
        dados = {chave: input_field.get() for chave, input_field in self.inputs.items()}
        
        # Exibe os dados capturados no terminal (console) para conferência
        print(f"Salvando Pessoa Física com CPF: {dados}")

        # Loop para limpar todos os campos após a coleta dos dados
        for input_field in self.inputs.values():
            input_field.delete(0, 'end') # Apaga do índice 0 até o final
            
        self.inputs["nome"].focus() # Coloca o cursor de digitação de volta no primeiro campo

# --- CLASSE PARA CADASTRO DE PESSOA JURÍDICA ---
class PessoaJuridica(ctk.CTkFrame): # Segue a mesma lógica de herança da Pessoa Física
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}

    def abrir_juridico(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        # Lista de campos específicos para Empresas (PJ)
        campos_pj = [
            ("Nome da Empresa:", "empresa", "Razão Social ou Nome Fantasia..."),
            ("CNPJ:", "cnpj", "00.000.000/0000-00"),
            ("Endereço:", "logradouro", "Endereço comercial..."),
            ("Número:", "numero", "Nº"),
            ("Bairro:", "bairro", "Bairro..."),
            ("Cidade:", "cidade", "Cidade..."),
            ("Estado:", "estado", "UF"),
            ("CEP:", "cep", "00000-000"),
            ("Telefone:", "telefone", "Telefone comercial..."),
            ("Email:", "email", "email@empresa.com")
        ]

        # Repete a criação dinâmica dos elementos visuais
        for i, (txt, chave, msg) in enumerate(campos_pj):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")

            entry = ctk.CTkEntry(
                self, width=400, height=40, font=("Arial", 16, "bold"),
                placeholder_text=msg, 
                fg_color="#F0F0F0", bg_color="white", border_width=0,
                corner_radius=50, text_color="black"
            )
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = entry

        # Botão de salvar para Pessoa Jurídica
        self.btn_salvar = ctk.CTkButton(
            self, text="SALVAR EMPRESA", fg_color="#2E8B57", hover_color="#145B06",
            font=("Arial", 14, "bold"), corner_radius=50, command=self.salvar_pj
        )
        self.btn_salvar.grid(row=len(campos_pj), column=1, pady=20, sticky="e", padx=5)

    def salvar_pj(self):
        # Coleta os dados usando compreensão de dicionário
        dados = {chave: input_field.get() for chave, input_field in self.inputs.items()}
        
        print(f"Salvando Pessoa Jurídica: {dados}")

        # Limpa todos os campos da tela de Pessoa Jurídica
        for input_field in self.inputs.values():
            input_field.delete(0, 'end') 
            
        self.inputs["empresa"].focus() # Devolve o foco para o primeiro campo (Empresa)
