import customtkinter as ctk
import database
from tkinter import messagebox
from datetime import datetime
import sqlite3

# =============================================================================
# JANELA DE DIÁLOGO PARA RECEBIMENTO (VALOR REAL E FORMA)
# =============================================================================
class JanelaReceber(ctk.CTkToplevel):
    """ Janela personalizada para confirmar o valor real recebido do cliente """
    def __init__(self, item_nome, valor_orig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x280")
        self.title("Confirmar Recebimento")
        self.configure(fg_color="#F0FFF0") # Verde claro (Honeydew)
        self.resizable(False, False)
        self.grab_set() 
        self.result = None

        ctk.CTkLabel(self, text=f"Receber de: {item_nome}", text_color="#145B06", 
                     font=("Arial", 13, "bold")).pack(pady=15)
        
        ctk.CTkLabel(self, text="Valor Real Recebido (R$):", text_color="black", font=("Arial", 11, "bold")).pack()
        self.ent_valor = ctk.CTkEntry(self, width=180, fg_color="white", border_color="#2E8B57", text_color="black", border_width=2)
        self.ent_valor.insert(0, f"{valor_orig:.2f}") 
        self.ent_valor.pack(pady=5)

        ctk.CTkLabel(self, text="Forma de Recebimento:", text_color="black", font=("Arial", 11, "bold")).pack()
        self.combo_forma = ctk.CTkComboBox(self, values=["Pix", "Dinheiro", "Cartão Débito", "Cartão Crédito", "Transferência"], 
                                           fg_color="white", border_color="#2E8B57", text_color="black", 
                                           button_color="#2E8B57", width=180)
        self.combo_forma.set("Pix")
        self.combo_forma.pack(pady=5)

        ctk.CTkButton(self, text="CONFIRMAR RECEBIMENTO", fg_color="#2E8B57", hover_color="#145B06",
                      font=("Arial", 11, "bold"), command=self.confirmar).pack(pady=20)

    def confirmar(self):
        self.result = {
            "valor_recebido": self.ent_valor.get().replace(",", "."),
            "forma": self.combo_forma.get()
        }
        self.destroy()

    def obter_dados(self):
        self.master.wait_window(self)
        return self.result

# =============================================================================
# MÓDULO PRINCIPAL: CONTAS A RECEBER
# =============================================================================
class ContasReceber(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.verde_escuro = "#145B06"
        self.verde_medio = "#2E8B57"
        self.laranja_busca = "#D2691E"
        self.branco = "white"
        self.cinza_fundo = "#F9F9F9"
        self.borda_cinza = "#E0E0E0"

    def abrir_contas_receber(self):
        self.garantir_tabela()
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color=self.branco)

        # --- CABEÇALHO ---
        header = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=50, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="💰 GESTÃO DE CONTAS A RECEBER", 
                     font=("Arial", 16, "bold"), text_color=self.branco).pack(pady=12)

        # --- FRAME 1: CADASTRO DE RECEBÍVEL ---
        self.frame_cad = ctk.CTkFrame(self, fg_color=self.cinza_fundo, border_width=1, border_color=self.borda_cinza)
        self.frame_cad.pack(fill="x", padx=20, pady=10)

        campos = [("Cliente", 0), ("Descrição/Serviço", 1), ("Vencimento", 2), ("Valor (R$)", 3)]
        self.entries = {}

        for texto, col in campos:
            cont = ctk.CTkFrame(self.frame_cad, fg_color="transparent")
            cont.grid(row=0, column=col, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(cont, text=texto, font=("Arial", 12, "bold"), text_color="black").pack(anchor="w")
            ent = ctk.CTkEntry(cont, width=170, fg_color=self.branco, border_color=self.verde_medio, text_color="black")
            ent.pack(pady=(2, 5))
            self.entries[texto] = ent

        self.btn_add = ctk.CTkButton(self.frame_cad, text="SALVAR", width=120, height=30,
                                   fg_color=self.verde_medio, hover_color=self.verde_escuro, 
                                   font=("Arial", 11, "bold"), command=self.registrar_recebivel)
        self.btn_add.grid(row=1, column=0, padx=10, pady=(5, 15), sticky="w") 

        # --- FRAME 2: BUSCA ---
        self.frame_busca = ctk.CTkFrame(self, fg_color=self.branco)
        self.frame_busca.pack(fill="x", padx=20, pady=5)

        self.entry_filtro = ctk.CTkEntry(self.frame_busca, placeholder_text="Filtrar por cliente ou O.S...", 
                                         width=300, border_color=self.verde_medio, fg_color=self.branco, text_color="black")
        self.entry_filtro.grid(row=0, column=0, padx=5)
        self.entry_filtro.bind("<KeyRelease>", lambda e: self.renderizar_tabela())

        ctk.CTkButton(self.frame_busca, text="🔍 BUSCAR", width=100, fg_color=self.laranja_busca, 
                      hover_color=self.verde_escuro, command=self.renderizar_tabela).grid(row=0, column=1, padx=5)

        # --- FRAME 3: TABELA DE RECEBÍVEIS ---
        self.frame_lista_header = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=30, corner_radius=5)
        self.frame_lista_header.pack(fill="x", padx=20, pady=(10,0))
        
        headers = [("CLIENTE", 230), ("DESCRIÇÃO", 150), ("VENCIMENTO", 90), ("VALOR", 100), ("STATUS", 90), ("AÇÃO", 100)]
        for i, (txt, w) in enumerate(headers):
            ctk.CTkLabel(self.frame_lista_header, text=txt, width=w, font=("Arial", 11, "bold"), text_color=self.branco).grid(row=0, column=i)

        self.scroll_receber = ctk.CTkScrollableFrame(self, fg_color=self.branco, height=300, border_width=1, border_color="#E0E0E0")
        self.scroll_receber.pack(fill="both", expand=True, padx=20, pady=(0,10))

        self.renderizar_tabela()

    def garantir_tabela(self):
        try:
            conn = sqlite3.connect("sistema_gestao.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS contas_receber (
                id_receber INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL, descricao TEXT NOT NULL, id_os_origem INTEGER, 
                data_vencimento TEXT NOT NULL, valor_total REAL NOT NULL,
                valor_recebido REAL DEFAULT 0, data_recebimento TEXT, 
                forma_recebimento TEXT, status TEXT DEFAULT 'PENDENTE')""")
            conn.commit(); conn.close()
        except: pass

    def registrar_recebivel(self):
        cli = self.entries["Cliente"].get().title()
        desc = self.entries["Descrição/Serviço"].get().title()
        venc = self.entries["Vencimento"].get()
        valor = self.entries["Valor (R$)"].get()
        
        if all([cli, desc, venc, valor]):
            dados = {"cliente": cli, "descricao": desc, "data_vencimento": venc, "valor_total": valor}
            if database.salvar_conta_receber(dados):
                messagebox.showinfo("Sucesso", "Título a receber cadastrado!")
                self.renderizar_tabela()
                for e in self.entries.values(): e.delete(0, 'end')
            else: messagebox.showerror("Erro", "Falha ao gravar no banco.")
        else: messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def renderizar_tabela(self):
        for widget in self.scroll_receber.winfo_children(): widget.destroy()
        contas = database.buscar_contas_receber_flexivel(self.entry_filtro.get())

        for c in contas:
            linha = ctk.CTkFrame(self.scroll_receber, fg_color="transparent")
            linha.pack(fill="x", pady=2)
            cor_status = "#B22222" if c['status'] == "PENDENTE" else "#2E8B57"

            ctk.CTkLabel(linha, text=c['cliente'], width=230, anchor="w", text_color="black").grid(row=0, column=0, padx=5)
            ctk.CTkLabel(linha, text=c['descricao'], width=150, anchor="w", text_color="black").grid(row=0, column=1)
            ctk.CTkLabel(linha, text=c['data_vencimento'], width=90, text_color="black").grid(row=0, column=2)
            ctk.CTkLabel(linha, text=f"R$ {c['valor_total']:.2f}", width=100, text_color="black", font=("Arial", 11, "bold")).grid(row=0, column=3)
            ctk.CTkLabel(linha, text=c['status'], width=90, text_color=cor_status, font=("Arial", 10, "bold")).grid(row=0, column=4)

            if c['status'] == "PENDENTE":
                ctk.CTkButton(linha, text="RECEBER", width=80, height=25, fg_color=self.verde_medio, hover_color=self.verde_escuro,
                            font=("Arial", 10, "bold"), command=lambda id_r=c['id_receber'], v=c['valor_total'], n=c['cliente']: self.dar_baixa(id_r, v, n)).grid(row=0, column=5, padx=5)
            else:
                ctk.CTkLabel(linha, text="RECEBIDO ✅", width=80, text_color=self.verde_medio, font=("Arial", 10, "italic")).grid(row=0, column=5)

    def dar_baixa(self, id_receber, valor_total, cliente):
        dialogo = JanelaReceber(cliente, valor_total, master=self)
        res = dialogo.obter_dados()
        
        if res:
            try:
                hoje = datetime.now().strftime("%d/%m/%Y")
                dados_baixa = {
                    "valor_recebido": float(res['valor_recebido']),
                    "data_recebimento": hoje,
                    "forma_recebimento": res['forma']
                }
                if database.baixar_conta_receber(id_receber, dados_baixa):
                    messagebox.showinfo("Sucesso", f"Recebimento registrado!\nValor: R$ {dados_baixa['valor_recebido']:.2f}")
                    self.renderizar_tabela()
            except ValueError:
                messagebox.showerror("Erro", "Valor numérico inválido.")
