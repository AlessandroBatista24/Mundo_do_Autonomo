import customtkinter as ctk
import database
from tkinter import messagebox
from datetime import datetime
import sqlite3

# =============================================================================
# JANELA DE DIÁLOGO PARA BAIXA (VALOR REAL E FORMA DE PAGAMENTO)
# =============================================================================
class JanelaBaixa(ctk.CTkToplevel):
    """ Janela personalizada para confirmar o valor real pago e forma de pagamento """
    def __init__(self, item_nome, valor_orig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x280")
        self.title("Confirmar Pagamento")
        self.configure(fg_color="#F0FFF0") # FUNDO VERDE BEM CLARO (Honeydew)
        self.resizable(False, False)
        self.grab_set() 
        self.result = None

        ctk.CTkLabel(self, text=f"Baixa de: {item_nome}", text_color="#145B06", 
                     font=("Arial", 13, "bold")).pack(pady=15)
        
        # Campo Valor Pago
        ctk.CTkLabel(self, text="Valor Real Pago (R$):", text_color="black", font=("Arial", 11, "bold")).pack()
        self.ent_valor = ctk.CTkEntry(self, width=180, fg_color="white", border_color="#2E8B57", 
                                     text_color="black", border_width=2)
        self.ent_valor.insert(0, f"{valor_orig:.2f}") 
        self.ent_valor.pack(pady=5)

        # Campo Forma de Pagamento
        ctk.CTkLabel(self, text="Forma de Pagamento:", text_color="black", font=("Arial", 11, "bold")).pack()
        self.combo_forma = ctk.CTkComboBox(self, values=["Dinheiro", "Pix", "Cartão Débito", "Transferência"], 
                                           fg_color="white", border_color="#2E8B57", text_color="black", 
                                           button_color="#2E8B57", button_hover_color="#145B06",
                                           dropdown_fg_color="white", dropdown_text_color="black",
                                           dropdown_hover_color="#98FB98", width=180) # Verde claro no hover
        self.combo_forma.set("Pix") # Pix como padrão por ser o mais comum em 2026
        self.combo_forma.pack(pady=5)

        ctk.CTkButton(self, text="CONFIRMAR PAGAMENTO", fg_color="#2E8B57", hover_color="#145B06",
                      text_color="white", font=("Arial", 11, "bold"), command=self.confirmar).pack(pady=20)

    def confirmar(self):
        self.result = {
            "valor_pago": self.ent_valor.get().replace(",", "."),
            "forma": self.combo_forma.get()
        }
        self.destroy()

    def obter_dados(self):
        self.master.wait_window(self)
        return self.result



# =============================================================================
# MÓDULO PRINCIPAL: CONTAS A PAGAR
# =============================================================================
class ContasPagar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.verde_escuro = "#145B06"
        self.verde_medio = "#2E8B57"
        self.laranja_busca = "#D2691E"
        self.branco = "white"
        self.cinza_fundo = "#F9F9F9"
        self.borda_cinza = "#E0E0E0"

    def abrir_contas_pagar(self):
        self.garantir_tabela()
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color=self.branco)

        # --- CABEÇALHO ---
        header = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=50, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="📑 GESTÃO DE CONTAS A PAGAR", 
                     font=("Arial", 16, "bold"), text_color=self.branco).pack(pady=12)

        # --- FRAME 1: CADASTRO DE CONTA ---
        self.frame_cad = ctk.CTkFrame(self, fg_color=self.cinza_fundo, border_width=1, border_color=self.borda_cinza)
        self.frame_cad.pack(fill="x", padx=20, pady=10)

        campos = [("Descrição", 0), ("Empresa Credora", 1), ("Vencimento", 2), ("Valor (R$)", 3)]
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
                                   font=("Arial", 11, "bold"), command=self.registrar_conta)
        self.btn_add.grid(row=1, column=0, padx=10, pady=(5, 15), sticky="w") 

        # --- FRAME 2: BUSCA ---
        self.frame_busca = ctk.CTkFrame(self, fg_color="white")
        self.frame_busca.pack(fill="x", padx=20, pady=5)

        self.entry_filtro = ctk.CTkEntry(self.frame_busca, placeholder_text="Filtrar contas...", 
                                         width=300, border_color=self.verde_medio, fg_color="white", text_color="black")
        self.entry_filtro.grid(row=0, column=0, padx=5)
        self.entry_filtro.bind("<KeyRelease>", lambda e: self.renderizar_tabela())

        btn_buscar = ctk.CTkButton(self.frame_busca, text="🔍 BUSCAR", width=100, fg_color=self.laranja_busca, 
                                      hover_color=self.verde_escuro, command=self.renderizar_tabela)
        btn_buscar.grid(row=0, column=1, padx=5)

        # --- FRAME 3: TABELA DE CONTAS (LARGURAS AJUSTADAS) ---
        self.frame_lista_header = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=30, corner_radius=5)
        self.frame_lista_header.pack(fill="x", padx=20, pady=(10,0))
        
        headers = [("DESCRIÇÃO", 230), ("CREDOR", 150), ("VENCIMENTO", 90), ("VALOR", 100), ("STATUS", 90), ("AÇÃO", 100)]
        for i, (txt, w) in enumerate(headers):
            ctk.CTkLabel(self.frame_lista_header, text=txt, width=w, font=("Arial", 11, "bold"), text_color="white").grid(row=0, column=i)

        self.scroll_contas = ctk.CTkScrollableFrame(self, fg_color="white", height=300, border_width=1, border_color="#E0E0E0")
        self.scroll_contas.pack(fill="both", expand=True, padx=20, pady=(0,10))

        self.renderizar_tabela()
        self.verificar_alertas()

    def garantir_tabela(self):
        try:
            conn = sqlite3.connect("sistema_gestao.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS contas_pagar (
                id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL, credor TEXT NOT NULL, data_vencimento TEXT NOT NULL,
                valor_original REAL NOT NULL, valor_pago REAL DEFAULT 0,
                data_pagamento TEXT, forma_pagamento TEXT, status TEXT DEFAULT 'PENDENTE')""")
            conn.commit(); conn.close()
        except: pass

    def registrar_conta(self):
        desc = self.entries["Descrição"].get().title()
        cred = self.entries["Empresa Credora"].get().title()
        venc = self.entries["Vencimento"].get()
        valor = self.entries["Valor (R$)"].get()
        
        if all([desc, cred, venc, valor]):
            dados = {"descricao": desc, "credor": cred, "data_vencimento": venc, "valor_original": valor}
            if database.salvar_conta_pagar(dados):
                messagebox.showinfo("Sucesso", "Conta financeira cadastrada!")
                self.renderizar_tabela()
                for e in self.entries.values(): e.delete(0, 'end')
            else: messagebox.showerror("Erro", "Falha ao gravar no banco.")
        else: messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def renderizar_tabela(self):
        for widget in self.scroll_contas.winfo_children(): widget.destroy()
        contas = database.buscar_contas_pagar_flexivel(self.entry_filtro.get())

        for c in contas:
            linha = ctk.CTkFrame(self.scroll_contas, fg_color="transparent")
            linha.pack(fill="x", pady=2)
            cor_status = "#B22222" if c['status'] == "PENDENTE" else "#2E8B57"

            ctk.CTkLabel(linha, text=c['descricao'], width=230, anchor="w", text_color="black").grid(row=0, column=0, padx=5)
            ctk.CTkLabel(linha, text=c['credor'], width=150, anchor="w", text_color="black").grid(row=0, column=1)
            ctk.CTkLabel(linha, text=c['data_vencimento'], width=90, text_color="black").grid(row=0, column=2)
            ctk.CTkLabel(linha, text=f"R$ {c['valor_original']:.2f}", width=100, text_color="black", font=("Arial", 11, "bold")).grid(row=0, column=3)
            ctk.CTkLabel(linha, text=c['status'], width=90, text_color=cor_status, font=("Arial", 10, "bold")).grid(row=0, column=4)

            if c['status'] == "PENDENTE":
                ctk.CTkButton(linha, text="BAIXA", width=80, height=25, fg_color=self.verde_medio, hover_color=self.verde_escuro,
                            font=("Arial", 10, "bold"), command=lambda id_c=c['id_conta'], v=c['valor_original'], d=c['descricao']: self.dar_baixa(id_c, v, d)).grid(row=0, column=5, padx=5)
            else:
                ctk.CTkLabel(linha, text="PAGO ✅", width=80, text_color=self.verde_medio, font=("Arial", 10, "italic")).grid(row=0, column=5)

    def dar_baixa(self, id_conta, valor_original, descricao):
        # Abre a janela de diálogo para confirmar valor real e forma de pagamento
        dialogo = JanelaBaixa(descricao, valor_original, master=self)
        res = dialogo.obter_dados()
        
        if res:
            try:
                hoje = datetime.now().strftime("%d/%m/%Y")
                # CORREÇÃO: O nome da chave deve ser 'forma_pagamento' para bater com o banco
                dados_baixa = {
                    "valor_pago": float(res['valor_pago']),
                    "data_pagamento": hoje,
                    "forma_pagamento": res['forma'] # Chave corrigida aqui
                }
                
                # Chama o banco passando o ID e o dicionário corrigido
                if database.baixar_conta_pagar(id_conta, dados_baixa):
                    messagebox.showinfo("Sucesso", "Pagamento registrado com sucesso!")
                    self.renderizar_tabela()
                else:
                    messagebox.showerror("Erro", "O banco de dados não confirmou a alteração.")
                    
            except ValueError:
                messagebox.showerror("Erro", "Valor de pagamento inválido.")
            except Exception as e:
                messagebox.showerror("Erro Crítico", f"Detalhe: {e}")

    def verificar_alertas(self):
        hoje = datetime.now().strftime("%d/%m/%Y")
        contas = database.buscar_contas_pagar_flexivel("")
        vencendo = [c['descricao'] for c in contas if c['data_vencimento'] == hoje and c['status'] == 'PENDENTE']
        if vencendo:
            messagebox.showwarning("VENCIMENTOS HOJE", f"Atenção! Faturas para hoje:\n\n- " + "\n- ".join(vencendo))
