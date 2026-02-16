import customtkinter as ctk
# Importação dos módulos específicos de cada tela para permitir a troca dinâmica
from clientes import PessoaFisica, PessoaJuridica
from produtos import Produtos, Servicos 

# --- CLASSE DO CABEÇALHO (BARRA SUPERIOR) ---
# Responsável pela identidade visual no topo do software
class ContainerSuperior(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Cria um Frame horizontal fixo no topo. Cores em Hexadecimal (#98FB98 = Verde Pálido)
        super().__init__(master, width=1000, height=130, bg_color="#98FB98",
                         fg_color="#98FB98", corner_radius=0, **kwargs)
        # Posicionamento absoluto no topo esquerdo (0,0)
        self.place(x=0, y=0)
        
        # Título do sistema. O uso de relx e rely=0.5 com anchor="center" garante 
        # que o texto fique perfeitamente centralizado, independente do tamanho do monitor.
        self.titulo = ctk.CTkLabel(self, text="Mundo do Autônomo!", text_color="#145B06", font=("Arial", 32, "bold"))
        self.titulo.place(relx=0.5, rely=0.5, anchor="center")

# --- CLASSE DO MENU LATERAL ---
# Gerencia a navegação e a lógica de troca de janelas
class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, interface_central, **kwargs):
        # Frame vertical à esquerda. Cores verdes levemente mais escuras que o topo
        super().__init__(master, width=180, height=620, bg_color="#7CCD7C",
                         fg_color="#7CCD7C", corner_radius=0, **kwargs) 
        
        # Recebe a referência da 'Interface' (o frame branco à direita) 
        # para saber onde as telas devem ser "desenhadas".
        self.interface_central = interface_central 
        
        # Posicionado logo abaixo do cabeçalho (y=130)
        self.place(x=0, y=130)
        
        # Grid_propagate(False) impede que o menu "encolha" ou "estique" 
        # caso os botões tenham tamanhos diferentes.
        self.grid_propagate(False)

        # --- BOTÕES DO MENU ---
        # Cada botão executa um comando 'self.abrir_...' que limpa a tela e carrega a nova
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
        
        # ... (Demais botões seguem o mesmo padrão de design e posicionamento em Grid)

    # --- MÉTODO PARA LIMPAR A TELA CENTRAL ---
    # Essencial para garantir que uma tela não fique em cima da outra
    def limpar_interface(self):
        # winfo_children() retorna uma lista de todos os elementos dentro da Interface
        for widget in self.interface_central.winfo_children():
            widget.destroy() # Remove o elemento e libera memória

    # --- MÉTODOS DE TROCA DE TELA ---
    # Seguem o padrão: Limpar -> Instanciar Classe da Tela -> Executar método de abertura
    def abrir_fisica(self):
        self.limpar_interface() 
        janela_fisica = PessoaFisica(master=self.interface_central)
        janela_fisica.abrir_fisica()

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

    # (Os demais métodos abaixo seguirão o mesmo padrão conforme você criar os arquivos correspondentes)
    # ...

# --- CLASSE DA INTERFACE (O PALCO ONDE TUDO APARECE) ---
# Este é o frame branco à direita que atua como o "conteúdo" do sistema
class Interface(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Definido com largura de 820 para ocupar o restante da janela (1000 total - 180 do menu)
        super().__init__(master, width=820, height=620, fg_color="white", corner_radius=0, **kwargs) 
        # O deslocamento x=180 evita que o frame fique escondido atrás do Menu Lateral
        self.place(x=180, y=130)
        # Trava o tamanho do frame para evitar que layouts internos o redimensionem
        self.grid_propagate(False)
