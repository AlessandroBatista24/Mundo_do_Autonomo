import customtkinter as ctk  # Importa a biblioteca da interface visual moderna
import database             # Importa as funções de banco de dados (SQL)
from tkinter import messagebox # Importa caixas de alerta do sistema

class Estoque(ctk.CTkFrame): # Classe que herda de CTkFrame (uma "sub-janela" dentro da principal)
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) # Inicializa as propriedades do Frame pai
        self.lista_cards = [] # Lista auxiliar para gerenciar os itens na tela

    def abrir_estoque(self):
        """Configura e exibe a tela de estoque no container central"""
        self.place(x=0, y=0, relwidth=1, relheight=1) # Faz o frame ocupar todo o espaço central
        self.configure(fg_color="white") # Define o fundo como branco

        # --- CABEÇALHO ---
        # Cria um retângulo verde no topo para o título
        header = ctk.CTkFrame(self, fg_color="#145B06", height=60, corner_radius=0)
        header.pack(fill="x") # Expande o cabeçalho horizontalmente
        # Adiciona o texto do título centralizado no cabeçalho
        ctk.CTkLabel(header, text="📦 CONSULTA DE ESTOQUE ATUAL", font=("Arial", 18, "bold"), text_color="white").pack(pady=15)

        # --- BARRA DE PESQUISA ---
        # Frame invisível para organizar a barra de busca e o botão limpar
        frame_busca = ctk.CTkFrame(self, fg_color="transparent")
        frame_busca.pack(fill="x", padx=20, pady=15)

        # Campo de entrada de texto para pesquisa
        self.entry_busca = ctk.CTkEntry(frame_busca, placeholder_text="Pesquise por produto ou fabricante...", 
                                        width=400, height=35, border_width=1, corner_radius=50,
                                        fg_color="white", text_color="black")
        self.entry_busca.pack(side="left", padx=10)
        
        # O bind executa 'carregar_itens' toda vez que o usuário solta uma tecla (pesquisa viva)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.carregar_itens()) 

        # Botão verde para resetar a pesquisa
        btn_limpar = ctk.CTkButton(frame_busca, text="LIMPAR", width=100, height=35, 
                                   fg_color="#2E8B57", hover_color="#145B06", corner_radius=50,
                                   command=self.limpar_busca)
        btn_limpar.pack(side="left", padx=5)

        # --- TABELA DE RESULTADOS ---
        # Frame cinza claro para servir de 'cabeçalho' da tabela (nomes das colunas)
        frame_titulos = ctk.CTkFrame(self, fg_color="#F0F0F0", height=35)
        frame_titulos.pack(fill="x", padx=20)
        
        # Configuração padrão para os textos das colunas
        estilo_titulo = {"font": ("Arial", 12, "bold"), "text_color": "black"}
        # Alinhamento das colunas usando Grid
        ctk.CTkLabel(frame_titulos, text="PRODUTO", width=250, anchor="w", **estilo_titulo).grid(row=0, column=0, padx=15)
        ctk.CTkLabel(frame_titulos, text="FABRICANTE", width=200, anchor="w", **estilo_titulo).grid(row=0, column=1)
        ctk.CTkLabel(frame_titulos, text="UNID.", width=80, **estilo_titulo).grid(row=0, column=2)
        ctk.CTkLabel(frame_titulos, text="QTD ATUAL", width=100, **estilo_titulo).grid(row=0, column=3)

        # Área com rolagem (scroll) onde os produtos serão listados
        self.scroll_estoque = ctk.CTkScrollableFrame(self, fg_color="white", scrollbar_button_color="#2E8B57")
        self.scroll_estoque.pack(fill="both", expand=True, padx=20, pady=5)

        # Chama a função para buscar e mostrar os itens assim que a tela abre
        self.carregar_itens()

    def carregar_itens(self):
        """Busca no banco de dados e desenha as linhas da tabela de estoque"""
        # Destrói os itens antigos da lista para não duplicar na tela
        for widget in self.scroll_estoque.winfo_children():
            widget.destroy()

        # Pega o texto da busca
        termo = self.entry_busca.get()
        # Chama a função SQL flexível que criamos no database.py
        produtos = database.buscar_produtos_flexivel(termo)

        if not produtos:
            return # Se não houver produtos, para a execução aqui

        # Loop para criar uma linha (card) para cada produto encontrado
        for p in produtos:
            # Container da linha com bordas sutis
            card = ctk.CTkFrame(self.scroll_estoque, fg_color="#F9F9F9", height=45, corner_radius=5, border_width=1, border_color="#EEEEEE")
            card.pack(fill="x", pady=2)
            card.pack_propagate(False) # Impede que o card mude de tamanho por causa do conteúdo

            # Dados do produto alinhados em colunas (grid)
            ctk.CTkLabel(card, text=p['produto'], font=("Arial", 13, "bold"), width=250, anchor="w", text_color="black").grid(row=0, column=0, padx=15, pady=10)
            ctk.CTkLabel(card, text=p['fabricante'], font=("Arial", 12), width=200, anchor="w", text_color="#333333").grid(row=0, column=1)
            ctk.CTkLabel(card, text=p['unidade'], font=("Arial", 12), width=80, text_color="black").grid(row=0, column=2)

            # Lógica de cor para a quantidade: vermelho se zero, verde se disponível
            qtd = p['quantidade']
            cor_qtd = "#E20B0B" if qtd <= 0 else "#145B06"
            ctk.CTkLabel(card, text=str(qtd), font=("Arial", 14, "bold"), width=100, text_color=cor_qtd).grid(row=0, column=3)

    def limpar_busca(self):
        """Limpa o campo de texto e recarrega a lista completa"""
        self.entry_busca.delete(0, 'end')
        self.carregar_itens()
