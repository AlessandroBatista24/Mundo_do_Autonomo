import customtkinter as ctk
from clientes import PessoaFisica, PessoaJuridica
from produtos import Produtos, Servicos 

# --- CLASSE DO CABEÇALHO (BARRA SUPERIOR) ---
class ContainerSuperior(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Cria o frame do topo com largura de 1000 e altura de 130
        super().__init__(master, width=1000, height=130, bg_color="#98FB98",
                         fg_color="#98FB98", corner_radius=0, **kwargs)
        # Posiciona o cabeçalho no ponto zero (topo esquerdo)
        self.place(x=0, y=0)
        
        # Cria o título principal centralizado no cabeçalho
        self.titulo = ctk.CTkLabel(self, text="Mundo do Autônomo!", text_color="#145B06", font=("Arial", 32, "bold"))
        self.titulo.place(relx=0.5, rely=0.5, anchor="center")

# --- CLASSE DO MENU LATERAL ---
class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, interface_central, **kwargs):
        # Cria o frame lateral com largura de 180 e altura de 620
        super().__init__(master, width=180, height=620, bg_color="#7CCD7C",
                         fg_color="#7CCD7C", corner_radius=0, **kwargs) 
        
        # Guarda a referência da 'Interface' central para poder desenhar nela depois
        self.interface_central = interface_central 
        
        # Posiciona o menu abaixo do cabeçalho (y=130)
        self.place(x=0, y=130)
        
        # Impede que o frame mude de tamanho automaticamente para "abraçar" os botões
        self.grid_propagate(False)

        # --- CRIAÇÃO DOS BOTÕES DO MENU ---
        # Cada botão chama uma função específica (command=self.abrir_...)
        self.fisico = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CADASTRO PES. FISICA", 
                                    font=("Century Gothic bold", 12), corner_radius=0, hover_color="#145B06", command=self.abrir_fisica)     
        self.fisico.grid(row=0, column=0, pady=2)

        self.juridico = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CADASTRO PES. JURIDICA", 
                                      font=("Century Gothic bold", 12), corner_radius=0, hover_color="#145B06", command=self.abrir_juridico)     
        self.juridico.grid(row=1, column=0, pady=2)  

        self.produtos_btn = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", hover_color="#145B06", text="CAD. PRODUTOS", 
                                      font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_produtos)
        self.produtos_btn.grid(row=2, column=0, pady=2)
        
        self.servicos_btn = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", hover_color="#145B06", text="CAD. SERVIÇOS", 
                                      font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_servicos)
        self.servicos_btn.grid(row=3, column=0, pady=2)

        self.estoque = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", hover_color="#145B06", text="ESTOQUE", 
                                     font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_estoque)
        self.estoque.grid(row=4, column=0, pady=2)

        self.orcamento = ctk.CTkButton(self, width=180, height=40, hover_color="#145B06", fg_color="#2E8B57", text="ORÇAMENTO", 
                                       font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_orcamento)     
        self.orcamento.grid(row=5, column=0, pady=2) 

        self.os = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", hover_color="#145B06", text="ORDEM DE SERVIÇO", 
                                font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_os)
        self.os.grid(row=6, column=0, pady=2)
        
        self.pagamento = ctk.CTkButton(self, width=180, height=40, hover_color="#145B06", fg_color="#2E8B57", text="PAGAMENTOS", 
                                       font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_contas_pagar)
        self.pagamento.grid(row=7, column=0, pady=2)

        self.recebimentos = ctk.CTkButton(self, width=180, height=40, hover_color="#145B06", fg_color="#2E8B57", text="RECEBIMENTOS", 
                                          font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_contas_receber)
        self.recebimentos.grid(row=8, column=0, pady=2)

        self.caixa_btn = ctk.CTkButton(self, width=180, height=40, hover_color="#145B06", fg_color="#2E8B57", text="CAIXA", 
                                     font=("Century Gothic bold", 12), corner_radius=0, command=self.abrir_caixa)
        self.caixa_btn.grid(row=9, column=0, pady=2)

    # --- MÉTODO PARA LIMPAR A TELA CENTRAL ---
    def limpar_interface(self):
        # Percorre todos os widgets (botões, campos, labels) da interface central e os destrói
        for widget in self.interface_central.winfo_children():
            widget.destroy()

    # --- MÉTODOS PARA TROCAR DE TELA ---
    def abrir_fisica(self):
        self.limpar_interface() # Remove a tela anterior
        # Cria a tela de Pessoa Física passando a interface central como 'mãe' (master)
        janela_fisica = PessoaFisica(master=self.interface_central)
        janela_fisica.abrir_fisica() # Desenha os campos na tela

    def abrir_juridico(self):
        self.limpar_interface()
        jan_juridico = PessoaJuridica(master=self.interface_central)
        jan_juridico.abrir_juridico()
        
    def abrir_produtos(self):
        self.limpar_interface()
        jan_produtos = Produtos(master=self.interface_central)
        jan_produtos.abrir_produtos()

    def abrir_servicos(self):
        self.limpar_interface()
        jan_servicos = Servicos(master=self.interface_central)
        jan_servicos.abrir_servicos()

    def abrir_estoque(self):
        self.limpar_interface()
        jan_estoque = estoque(master=self.interface_central)
        jan_estoque.abrir_estoque()

    def abrir_orcamento(self):
        self.limpar_interface()
        jan_orcamento = Orcamento(master=self.interface_central)
        jan_orcamento.abrir_orcamento()

    def abrir_os(self):
        self.limpar_interface()
        jan_os = OrdemDeServico(master=self.interface_central)
        jan_os.abrir_os()

    def abrir_contas_pagar(self):
        self.limpar_interface()
        jan_contas_pagar = ContasPagar(master=self.interface_central)
        jan_contas_pagar.abrir_contas_pagar()

    def abrir_contas_receber(self):
        self.limpar_interface()
        jan_contas_receber = ContasReceber(master=self.interface_central)
        jan_contas_receber.abrir_contas_receber()

    def abrir_caixa(self):
        self.limpar_interface()
        jan_caixa = Caixa(master=self.interface_central)
        jan_caixa.abrir_caixa()

# --- CLASSE DA INTERFACE (O PALCO ONDE TUDO APARECE) ---
class Interface(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Cria o frame que ficará à direita do menu e abaixo do cabeçalho
        super().__init__(master, width=820, height=620, fg_color="white", corner_radius=0, **kwargs) 
        # Posiciona a interface central (x=180 para não ficar atrás do menu)
        self.place(x=180, y=130)
        # Garante que ela mantenha o tamanho fixo definido
        self.grid_propagate(False)
