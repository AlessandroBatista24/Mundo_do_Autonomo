import customtkinter as ctk # Importa a biblioteca para criar janelas modernas com suporte a temas
from container import ContainerSuperior, MenuLateral, Interface # Importa os módulos de layout
import database # Importa o banco de dados para garantir a inicialização

# --- CLASSE QUE GERA A JANELA PRINCIPAL DO SISTEMA ---
# Esta classe herda de ctk.CTk, tornando-se o "corpo" principal da aplicação (Root Window)
class Criando_janela(ctk.CTk):
    def __init__(self):
        super().__init__() # Executa a inicialização obrigatória da classe pai (ctk.CTk)
        
        # Garante que o arquivo de banco de dados e as tabelas sejam criados ao abrir o app
        database.criar_banco()
        
        # Configura as propriedades visuais da janela (tamanho, título e centralização)
        self.configuracoes_janela_principal()
        
        # --- INSTANCIAÇÃO DOS COMPONENTES (COMPOSIÇÃO DE OBJETOS) ---
        
        # Instancia a barra superior (Frame de Cabeçalho)
        # master=self indica que este componente pertence a esta janela
        self.header = ContainerSuperior(master=self)
        
        # Instancia a área central (Frame de Interface) onde o conteúdo dinâmico será exibido
        self.interface = Interface(master=self)
        
        # Instancia o Menu Lateral
        # Passamos a 'self.interface' como argumento para que o menu tenha a referência 
        # necessária para trocar as telas dentro do frame central.
        self.menu_lateral = MenuLateral(master=self, interface_central=self.interface)

    def configuracoes_janela_principal(self):
        """Define o comportamento físico e visual da janela raiz."""
        largura, altura = 1000, 750
        
        # Lógica de Centralização:
        # winfo_screenwidth() e winfo_screenheight() capturam a resolução do seu monitor.
        # Subtraímos metade do tamanho da janela da metade da tela para encontrar o ponto central.
        pos_x = (self.winfo_screenwidth() // 2) - (largura // 2)
        pos_y = (self.winfo_screenheight() // 2) - (altura // 2)
        
        # Aplica o tamanho e a posição na tela usando o formato de string Geometria: "LxA+X+Y"
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        # Define o título que aparece na barra superior do sistema operacional
        self.title("Assistente para Autônomos!")
        
        # Opcional: Impede que o usuário redimensione a janela de forma bagunçada
        self.resizable(False, False)
