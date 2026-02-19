import customtkinter as ctk        # Biblioteca para interface moderna (CustomTkinter)
from PIL import Image               # Biblioteca Pillow para manipulação de imagens (Logotipo)
from clientes import PessoaFisica, PessoaJuridica  # Importa as classes de clientes
from produtos import Produtos, Servicos            # Importa as classes de produtos/serviços
from estoque import Estoque          # Importa a nova classe de controle de estoque
from orcamento import Orcamentos  # Importa a nova classe que você está criando
from os_modulo import OS  # Importa a classe do novo arquivo que vamos criar
from cont_pagar import ContasPagar  # Agora o Python vai achar o arquivo cont_pagar.py
from cont_receber import ContasReceber  # Certifique-se que o nome do arquivo seja cont_receber.py

# =============================================================================
# CLASSE: CABEÇALHO (LOGO E TÍTULO)
# =============================================================================
class ContainerSuperior(ctk.CTkFrame):
    """ Define a barra superior do programa com o logo e o título do sistema. """
    def __init__(self, master, **kwargs):
        # Inicializa o frame com as cores e dimensões definidas
        super().__init__(master, width=1000, height=130, bg_color="#98FB98", fg_color="#98FB98", corner_radius=0, **kwargs)
        self.place(x=0, y=0) # Fixa no topo absoluto da janela
        
        # Bloco Try/Except para carregar a imagem (evita que o programa feche se a imagem sumir)
        try:
            self.logo_img = ctk.CTkImage(light_image=Image.open("imagem.png"), size=(90, 90))
        except: 
            self.logo_img = None # Se a imagem não for encontrada, o label funcionará apenas com texto
            
        # Título principal do software com o ícone (se houver) posicionado à esquerda (left)
        self.titulo = ctk.CTkLabel(self, text=" Mundo do Autônomo!", image=self.logo_img, 
                                   compound="left", padx=50, text_color="#145B06", font=("Arial", 32, "bold"))
        self.titulo.place(relx=0.5, rely=0.5, anchor="center") # Centraliza o título no frame

# =============================================================================
# CLASSE: MENU LATERAL (NAVEGAÇÃO)
# =============================================================================
class MenuLateral(ctk.CTkFrame):
    """ Gerencia os botões laterais e a lógica de troca de telas no container central. """
    def __init__(self, master, interface_central, **kwargs):
        # Configura o frame lateral (cor de fundo e dimensões)
        super().__init__(master, width=180, height=620, bg_color="#7CCD7C", fg_color="#7CCD7C", corner_radius=0, **kwargs) 
        self.interface_central = interface_central # Referência do frame onde as telas serão desenhadas
        self.place(x=0, y=130) # Posiciona logo abaixo do cabeçalho
        self.grid_propagate(False) # Impede que o frame mude de tamanho para caber os botões

        # Lista de configuração para criar os botões em loop (Texto do botão, Função correspondente)
        opcoes = [
            ("CADASTRO PES. FISICA", self.abrir_fisica),
            ("CADASTRO PES. JURIDICA", self.abrir_juridico),
            ("CAD. PRODUTOS", self.abrir_produtos),
            ("CAD. SERVIÇOS", self.abrir_servicos),
            ("ESTOQUE", self.abrir_estoque),
            ("ORÇAMENTO", self.abrir_orcamento),
            ("ORDEM DE SERVIÇO", self.abrir_os),
            ("CONTAS A PAGAR", self.abrir_contas_pagar),
            ("CONTAS A RECEBER", self.abrir_contas_receber),
            ("CAIXA", self.abrir_caixa),
        ]

        # Criação automatizada dos botões no menu lateral
        for i, (texto, comando) in enumerate(opcoes):
            btn = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text=texto, 
                                font=("Century Gothic bold", 11), corner_radius=0, 
                                hover_color="#145B06", command=comando)
            btn.grid(row=i, column=0, pady=2) # Organiza um abaixo do outro com pequeno espaçamento

    def limpar_interface(self):
        """ Destrói todos os widgets ativos no centro da tela antes de abrir uma nova tela. 
            Isso evita que uma tela seja desenhada por cima da outra. """
        for widget in self.interface_central.winfo_children():
            widget.destroy()

    # --- MÉTODOS DE NAVEGAÇÃO ---
    # Cada método limpa a tela central, instancia a classe necessária e chama seu método 'abrir'

    def abrir_fisica(self):
        self.limpar_interface()
        PessoaFisica(master=self.interface_central).abrir_fisica()

    def abrir_juridico(self):
        self.limpar_interface()
        PessoaJuridica(master=self.interface_central).abrir_juridico()

    def abrir_produtos(self):
        self.limpar_interface()
        Produtos(master=self.interface_central).abrir_produtos()

    def abrir_servicos(self):
        self.limpar_interface()
        Servicos(master=self.interface_central).abrir_servicos()

    def abrir_estoque(self):
        """ Carrega o módulo de consulta de estoque. """
        self.limpar_interface()
        janela = Estoque(master=self.interface_central)
        janela.abrir_estoque()

    # Placeholders (espaços reservados) para funções que ainda serão desenvolvidas
    def abrir_orcamento(self):
        self.limpar_interface()
        # Cria a instância da tela de orçamentos e chama o método para desenhá-la
        Orcamentos(master=self.interface_central).abrir_orcamento()

    def abrir_os(self):
        """ Limpa a interface central e carrega o módulo de Ordens de Serviço """
        self.limpar_interface()
        # Usamos 'interface_central' para manter a consistência com os outros métodos
        janela = OS(master=self.interface_central)
        janela.abrir_os() # Método que criaremos dentro do arquivo os_modulo.py


    def abrir_contas_pagar(self):
        """ Limpa a interface central e carrega o módulo de Contas a Pagar """
        self.limpar_interface()
        # Chama a classe ContasPagar que está dentro do seu arquivo cont_pagar.py
        janela = ContasPagar(master=self.interface_central)
        janela.abrir_contas_pagar() 

    def abrir_contas_receber(self):
        """ Limpa a interface central e carrega o módulo de Contas a Receber """
        # 1. Limpa o que estiver na tela agora
        self.limpar_interface()
        
        # 2. Importa a classe do arquivo que você criou (ajuste o nome do arquivo se necessário)
        from cont_receber import ContasReceber 
        
        # 3. Instancia a tela passando a interface central como 'palco'
        janela = ContasReceber(master=self.interface_central)
        
        # 4. Chama o método que desenha os campos e a tabela de recebíveis
        janela.abrir_contas_receber()


    def abrir_caixa(self): self.limpar_interface(); print("Caixa aberto")

# =============================================================================
# CLASSE: INTERFACE CENTRAL (O PALCO)
# =============================================================================
class Interface(ctk.CTkFrame):
    """ Este é o frame 'vazio' que fica no centro da tela. 
        Ele serve de base (master) para todas as outras telas do sistema. """
    def __init__(self, master, **kwargs):
        super().__init__(master, width=820, height=620, fg_color="white", corner_radius=0, **kwargs)
        self.place(x=180, y=130) # Posiciona ao lado do menu lateral
