import customtkinter as ctk
from container import ContainerSuperior, MenuLateral, Interface


class Criando_janela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracoes_janela_principal()
        
        # Instancia o container passando 'self' (esta janela) como master
        self.header = ContainerSuperior(master=self)
        self.menu_lateral = MenuLateral(master=self)
        self.interface = Interface(master=self)

    def configuracoes_janela_principal(self):
        largura, altura = 1000, 750
        pos_x = (self.winfo_screenwidth() // 2) - (largura // 2)
        pos_y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.title("Assistente para Autônomos!")

