import customtkinter as ctk # Biblioteca principal para a interface visual moderna
import database # Importa o módulo local de banco de dados para persistência das informações

# --- CLASSE PARA CADASTRO DE PESSOA FÍSICA ---
# Esta classe herda de CTkFrame, tornando-se um "container" que pode ser acoplado na janela principal
class PessoaFisica(ctk.CTkFrame): 
    def __init__(self, master, **kwargs):
        # O construtor inicializa o Frame dentro do elemento 'master' (geralmente a Interface central)
        super().__init__(master, **kwargs) 
        # self.inputs armazena os objetos 'Entry' (caixas de texto) para que possamos ler os dados depois
        self.inputs = {} 

    def abrir_fisica(self):
        # Define que o frame preencherá 100% da área disponível na interface central
        self.place(x=0, y=0, relwidth=1, relheight=1) 
        self.configure(fg_color="white") # Define o fundo da tela como branco

        # Estrutura de dados (Lista de Tuplas) para automação da criação dos campos
        # Formato: (Rótulo visível, Chave para o dicionário, Mensagem interna/Placeholder)
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

        # Loop 'enumerate' para iterar sobre a lista e criar widgets dinamicamente
        for i, (txt, chave, msg) in enumerate(campos_pf):
            # Cria o Rótulo (Label) com fonte Arial, Negrito e cor verde escura
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06")
            # Posicionamento via GRID: 'row=i' garante que cada campo fique em uma linha nova
            label.grid(row=i, column=0, padx=(10, 5), pady=3, sticky="w") 

            # Cria a Caixa de Entrada (Entry) com design arredondado (corner_radius=50)
            entry = ctk.CTkEntry(
                self, width=400, height=40, font=("Arial", 14, "bold"),
                placeholder_text=msg, 
                fg_color="#F0F0F0", bg_color="white", border_width=0,
                corner_radius=50, text_color="black" 
            )
            # Posiciona a Entry na coluna 1, ao lado do Label correspondente
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w") 
            # Registra o widget no dicionário usando a 'chave' (ex: self.inputs['nome'] = entry)
            self.inputs[chave] = entry 

        # Cria o botão SALVAR com efeito hover (muda de cor ao passar o mouse)
        self.btn_salvar = ctk.CTkButton(
            self, text="SALVAR", fg_color="#2E8B57", hover_color="#145B06",
            font=("Arial", 14, "bold"), corner_radius=50, command=self.salvar_pf
        )
        # Posiciona o botão na linha seguinte ao último campo (row=len(campos_pf))
        self.btn_salvar.grid(row=len(campos_pf), column=1, pady=20, sticky="e", padx=5)

    def salvar_pf(self):
        # Dicionário por compreensão: Lê o conteúdo de cada Entry e associa à sua chave
        dados = {chave: input_field.get() for chave, input_field in self.inputs.items()}
        
        # Envia o dicionário para a função de inserção no banco de dados SQLite
        database.salvar_cliente_pf(dados) 
        
        # Limpa o texto de todos os campos após a gravação
        for input_field in self.inputs.values():
            input_field.delete(0, 'end')
        
        # Devolve o foco do teclado para o primeiro campo (Nome) para agilizar o próximo cadastro
        self.inputs["nome"].focus()

# --- CLASSE PARA CADASTRO DE PESSOA JURÍDICA ---
# Segue a mesma lógica estrutural da Pessoa Física, mudando apenas os campos específicos
class PessoaJuridica(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}

    def abrir_juridico(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        campos_pj = [
            ("Nome da Empresa:", "empresa", "Razão Social da Empresa ..."),
            ("Nome Fantasia:", "fantasia", "Nome Fantasia da Empresa..."),
            ("CNPJ:", "cnpj", "00.000.000/0000-00"),
            ("INSCRIÇÃO:", "inscricao", "xxx.xxx.xx-x"),
            ("Endereço:", "logradouro", "Endereço comercial..."),
            ("Número:", "numero", "Nº"),
            ("Bairro:", "bairro", "Bairro..."),
            ("Cidade:", "cidade", "Cidade..."),
            ("Estado:", "estado", "UF"),
            ("CEP:", "cep", "00000-000"),
            ("Telefone:", "telefone", "Telefone comercial..."),
            ("Email:", "email", "email@empresa.com")
        ]

        # Processamento idêntico ao de PF para manter a identidade visual do sistema
        for i, (txt, chave, msg) in enumerate(campos_pj):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=3, sticky="w")

            entry = ctk.CTkEntry(
                self, width=400, height=40, font=("Arial", 14, "bold"),
                placeholder_text=msg, 
                fg_color="#F0F0F0", bg_color="white", border_width=0,
                corner_radius=50, text_color="black"
            )
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="w")
            self.inputs[chave] = entry

        self.btn_salvar = ctk.CTkButton(
            self, text="SALVAR", fg_color="#2E8B57", hover_color="#145B06",
            font=("Arial", 14, "bold"), corner_radius=50, command=self.salvar_pj
        )
        self.btn_salvar.grid(row=len(campos_pj), column=1, pady=20, sticky="e", padx=5)

    def salvar_pj(self):
        # Coleta dados, salva no banco de dados e limpa a interface de Pessoa Jurídica
        dados = {chave: input_field.get() for chave, input_field in self.inputs.items()}
        database.salvar_cliente_pj(dados) 
        
        for input_field in self.inputs.values():
            input_field.delete(0, 'end') 
            
        self.inputs["empresa"].focus()
