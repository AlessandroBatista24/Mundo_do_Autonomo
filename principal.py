import customtkinter as ctk # Importa a biblioteca CustomTkinter para a interface gráfica
from container import ContainerSuperior, MenuLateral, Interface # Importa as classes que criamos no arquivo container

# --- CLASSE QUE GERA A JANELA PRINCIPAL DO SISTEMA ---
class Criando_janela(ctk.CTk): # Criando_janela herda de CTk, que é a janela base do sistema
    def __init__(self):
        super().__init__() # Inicializa as configurações básicas do CustomTkinter
        
        # Chama o método que define o visual externo da janela (tamanho e título)
        self.configuracoes_janela_principal()
        
        # --- INSTANCIAÇÃO DOS COMPONENTES (ORGANIZAÇÃO) ---
        
        # Cria a barra superior (Cabeçalho) passando 'self' (esta janela) como mestre
        self.header = ContainerSuperior(master=self)
        
        # Cria a área central branca (Interface) onde as telas de cadastro vão aparecer
        self.interface = Interface(master=self)
        
        # Cria o menu lateral e passa a 'self.interface' como argumento.
        # Isso permite que o menu lateral saiba exatamente onde deve desenhar as novas telas.
        self.menu_lateral = MenuLateral(master=self, interface_central=self.interface)

    def configuracoes_janela_principal(self):
        # Define as dimensões desejadas para a janela
        largura, altura = 1000, 750
        
        # Cálculos matemáticos para descobrir o centro da tela do seu monitor
        # winfo_screenwidth() pega a largura total da sua tela real
        pos_x = (self.winfo_screenwidth() // 2) - (largura // 2)
        pos_y = (self.winfo_screenheight() // 2) - (altura // 2)
        
        # Define a geometria: "LARGURAxALTURA + POSIÇÃO_X + POSIÇÃO_Y"
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        # Define o texto que aparece na barra de título da janela
        self.title("Assistente para Autônomos!")
