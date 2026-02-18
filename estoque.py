import customtkinter as ctk
import database
from tkinter import messagebox

class Estoque(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def abrir_estoque(self):
        """Configura e exibe a tela de estoque no container central"""
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        # --- CABEÇALHO ---
        header = ctk.CTkFrame(self, fg_color="#145B06", height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="📦 CONSULTA DE ESTOQUE ATUAL", font=("Arial", 18, "bold"), text_color="white").pack(pady=15)

        # --- BARRA DE PESQUISA ---
        frame_busca = ctk.CTkFrame(self, fg_color="transparent")
        frame_busca.pack(fill="x", padx=20, pady=15)

        self.entry_busca = ctk.CTkEntry(frame_busca, placeholder_text="Pesquise por produto ou fabricante...", 
                                        width=400, height=35, border_width=1, corner_radius=50,
                                        fg_color="white", text_color="black")
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.carregar_itens()) 

        # --- ÁREA DE ROLAGEM ---
        self.scroll_estoque = ctk.CTkScrollableFrame(self, fg_color="white", scrollbar_button_color="#2E8B57")
        self.scroll_estoque.pack(fill="both", expand=True, padx=20, pady=5)

        self.carregar_itens()

    def carregar_itens(self):
        """Busca no banco e desenha as linhas do estoque"""
        for widget in self.scroll_estoque.winfo_children():
            widget.destroy()

        termo = self.entry_busca.get()
        produtos = database.buscar_produtos_flexivel(termo)

        if not produtos: return

        for p in produtos:
            card = ctk.CTkFrame(self.scroll_estoque, fg_color="#F9F9F9", height=45, corner_radius=5, border_width=1, border_color="#EEEEEE")
            card.pack(fill="x", pady=2)
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=p['produto'], font=("Arial", 13, "bold"), width=250, anchor="w", text_color="black").grid(row=0, column=0, padx=15, pady=10)
            ctk.CTkLabel(card, text=p['fabricante'], font=("Arial", 12), width=200, anchor="w", text_color="#333333").grid(row=0, column=1)
            
            qtd = p['quantidade']
            cor_qtd = "#E20B0B" if qtd <= 0 else "#145B06"
            ctk.CTkLabel(card, text=f"Qtd: {qtd}", font=("Arial", 14, "bold"), width=100, text_color=cor_qtd).grid(row=0, column=3)
