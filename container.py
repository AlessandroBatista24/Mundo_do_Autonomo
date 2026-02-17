import customtkinter as ctk 
from PIL import Image
from clientes import PessoaFisica, PessoaJuridica
from produtos import Produtos, Servicos 

class ContainerSuperior(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=1000, height=130, bg_color="#98FB98", fg_color="#98FB98", corner_radius=0, **kwargs)
        self.place(x=0, y=0)
        try:
            self.logo_img = ctk.CTkImage(light_image=Image.open("imagem.png"), size=(90, 90))
        except: self.logo_img = None
        self.titulo = ctk.CTkLabel(self, text=" Mundo do Autônomo!", image=self.logo_img, compound="left", padx=50, text_color="#145B06", font=("Arial", 32, "bold"))
        self.titulo.place(relx=0.5, rely=0.5, anchor="center")

class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, interface_central, **kwargs):
        super().__init__(master, width=180, height=620, bg_color="#7CCD7C", fg_color="#7CCD7C", corner_radius=0, **kwargs) 
        self.interface_central = interface_central 
        self.place(x=0, y=130)
        self.grid_propagate(False)

        # Agora cada botão tem sua função dedicada que limpa a tela
        self.btn_pf = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CADASTRO PES. FISICA", 
                                    font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_fisica)
        self.btn_pf.grid(row=0, column=0, pady=2)

        self.btn_pj = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CADASTRO PES. JURIDICA", 
                                    font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_juridico)
        self.btn_pj.grid(row=1, column=0, pady=2)

        self.btn_prod = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CAD. PRODUTOS", 
                                      font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_produtos)
        self.btn_prod.grid(row=2, column=0, pady=2)

        self.btn_serv = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CAD. SERVIÇOS", 
                                      font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_servicos)
        self.btn_serv.grid(row=3, column=0, pady=2)

        self.btn_est = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="ESTOQUE", 
                                     font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_estoque)
        self.btn_est.grid(row=4, column=0, pady=2)

        self.btn_orc = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="ORÇAMENTO", 
                                     font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_orcamento)
        self.btn_orc.grid(row=5, column=0, pady=2)

        self.btn_os = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="ORDEM DE SERVIÇO", 
                                    font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_os)
        self.btn_os.grid(row=6, column=0, pady=2)

        self.btn_pagar = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CONTAS A PAGAR", 
                                       font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_contas_pagar)
        self.btn_pagar.grid(row=7, column=0, pady=2)

        self.btn_receber = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CONTAS A RECEBER", 
                                         font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_contas_receber)
        self.btn_receber.grid(row=8, column=0, pady=2)

        self.btn_caixa = ctk.CTkButton(self, width=180, height=40, fg_color="#2E8B57", text="CAIXA", 
                                       font=("Century Gothic bold", 11), corner_radius=0, hover_color="#145B06", command=self.abrir_caixa)
        self.btn_caixa.grid(row=9, column=0, pady=2)

    def limpar_interface(self):
        """Remove absolutamente todos os widgets da tela central"""
        for widget in self.interface_central.winfo_children():
            widget.destroy()

    # --- FUNÇÕES DE ABERTURA ---
    def abrir_fisica(self):
        self.limpar_interface()
        janela = PessoaFisica(master=self.interface_central)
        janela.abrir_fisica()

    def abrir_juridico(self):
        self.limpar_interface()
        janela = PessoaJuridica(master=self.interface_central)
        janela.abrir_juridico()

    def abrir_produtos(self):
        self.limpar_interface()
        janela = Produtos(master=self.interface_central)
        janela.abrir_produtos()

    def abrir_servicos(self):
        self.limpar_interface()
        janela = Servicos(master=self.interface_central)
        janela.abrir_servicos()

    # Placeholders que também limpam a tela
    def abrir_estoque(self): self.limpar_interface(); print("Estoque aberto")
    def abrir_orcamento(self): self.limpar_interface(); print("Orçamento aberto")
    def abrir_os(self): self.limpar_interface(); print("OS aberta")
    def abrir_contas_pagar(self): self.limpar_interface(); print("Contas a pagar aberto")
    def abrir_contas_receber(self): self.limpar_interface(); print("Contas a receber aberto")
    def abrir_caixa(self): self.limpar_interface(); print("Caixa aberto")

class Interface(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=820, height=620, fg_color="white", corner_radius=0, **kwargs)
        self.place(x=180, y=130)
