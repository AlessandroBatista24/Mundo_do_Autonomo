import customtkinter as ctk
import database
from tkinter import messagebox
from datetime import datetime

class Caixa(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=0, **kwargs)
        self.verde_escuro = "#145B06"
        self.verde_medio = "#2E8B57"
        self.laranja_busca = "#D2691E"
        self.cinza_fundo = "#F9F9F9"
        self.borda_cinza = "#E0E0E0"
        self.cor_destaque_aporte = "#E6F3FF"

    def abrir_caixa(self):
        database.criar_tabela_caixa()
        self.place(x=0, y=0, relwidth=1, relheight=1)

        # --- CABEÇALHO PRINCIPAL ---
        header = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="💰 MOVIMENTAÇÃO DO DIA", 
                     font=("Arial", 20, "bold"), text_color="white").pack(pady=15)

        # --- DASHBOARD (CARDS) ---
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent", height=110)
        self.frame_cards.pack(fill="x", padx=20, pady=10)
        self.frame_cards.pack_propagate(False)
        self.atualizar_saldos()

        # --- ÁREA DE LANÇAMENTO (Simplificada) ---
        self.frame_add = ctk.CTkFrame(self, fg_color=self.cinza_fundo, border_width=1, border_color=self.borda_cinza)
        self.frame_add.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.frame_add, text="Descrição do Aporte:", font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        self.ent_desc = ctk.CTkEntry(self.frame_add, width=280, height=35, fg_color="white", border_color=self.verde_medio, text_color="black")
        self.ent_desc.grid(row=1, column=0, padx=10, pady=(0,10))

        ctk.CTkLabel(self.frame_add, text="Categoria:", font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=1, padx=10, pady=(5,0), sticky="w")
        self.combo_cat = ctk.CTkComboBox(self.frame_add, values=["INICIAL", "EMPR.", "INVEST."], 
                                         width=140, height=35, fg_color="white", border_color=self.verde_medio, 
                                         button_color=self.verde_medio, text_color="black")
        self.combo_cat.set("INVEST.")
        self.combo_cat.grid(row=1, column=1, padx=10, pady=(0,10))

        ctk.CTkLabel(self.frame_add, text="Valor R$:", font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=2, padx=10, pady=(5,0), sticky="w")
        self.ent_val = ctk.CTkEntry(self.frame_add, width=120, height=35, fg_color="white", border_color=self.verde_medio, text_color="black", font=("Arial", 14, "bold"))
        self.ent_val.grid(row=1, column=2, padx=10, pady=(0,10))

        self.btn_lancar = ctk.CTkButton(self.frame_add, text="LANÇAR APORTE", fg_color=self.verde_medio, 
                                        hover_color=self.verde_escuro, font=("Arial", 12, "bold"), height=35, command=self.salvar_aporte)
        self.btn_lancar.grid(row=1, column=3, padx=20, pady=(0,10))

        # --- FILTRO DE BUSCA (Apenas Texto) ---
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(fill="x", padx=20, pady=10)
        
        self.ent_busca = ctk.CTkEntry(self.frame_filtros, placeholder_text="🔍 Filtrar na lista de hoje (Nome, O.S., Conta)...", 
                                      width=450, height=35, fg_color="white", 
                                      border_color=self.verde_medio, text_color="black")
        self.ent_busca.pack(side="left", padx=5)
        self.ent_busca.bind("<KeyRelease>", lambda e: self.renderizar_tabela())

        # --- CABEÇALHO DA TABELA ---
        self.frame_label_tabela = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=35, corner_radius=5)
        self.frame_label_tabela.pack(fill="x", padx=20, pady=(10,0))
        
        titulos = [("HORA/DATA", 100), ("ORIGEM/CLIENTE", 160), ("DESCRIÇÃO", 240), ("FORMA", 110), ("VALOR", 130)]
        for i, (txt, w) in enumerate(titulos):
            ctk.CTkLabel(self.frame_label_tabela, text=txt, width=w, font=("Arial", 11, "bold"), text_color="white").grid(row=0, column=i)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="white", border_width=1, border_color=self.borda_cinza)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0,15))
        
        self.renderizar_tabela()

    def renderizar_tabela(self):
        # 1. Limpa a tela
        for w in self.scroll.winfo_children(): w.destroy()
        
        # 2. Pega a data de hoje de duas formas para garantir
        hoje_com_zero = datetime.now().strftime("%d/%m/%Y") # 21/02/2026
        hoje_sem_zero = datetime.now().strftime("%d/%m/%Y").replace("/0", "/") # 21/2/2026
        
        termo = self.ent_busca.get().upper().strip()

        # 3. Busca os dados brutos do banco
        movs = database.buscar_extrato_caixa() 

        encontrou_algo = False
        for m in movs:
            # Pega a data do item e limpa espaços
            data_item = str(m.get('data') or "").strip()

            # --- O FILTRO DE HOJE (Mais flexível) ---
            # Se a data do banco não for hoje (com ou sem zero), pula para o próximo
            if data_item != hoje_com_zero and data_item != hoje_sem_zero:
                continue
            
            # --- FILTRO DE BUSCA POR TEXTO ---
            if termo and termo not in str(m).upper():
                continue

            encontrou_algo = True
            # ... (Resto do seu código de desenho da linha: bg, txt_valor, f.pack, etc) ...
            
            # --- CÓDIGO DE DESENHO DA LINHA (Mantenha o seu que já funcionava) ---
            bg = self.cor_destaque_aporte if m['tipo'] == 'APORTE' else "white"
            txt_valor = "#145B06" if m['tipo'] in ['ENTRADA', 'APORTE'] else "#B22222"
            f = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=0, height=45)
            f.pack(fill="x", pady=1); f.pack_propagate(False)
            
            ctk.CTkLabel(f, text=data_item, width=100, font=("Arial", 12), text_color="black").grid(row=0, column=0, pady=8)
            ctk.CTkLabel(f, text=str(m['origem'])[:20], width=160, anchor="w", font=("Arial", 12, "bold"), text_color="black").grid(row=0, column=1)
            ctk.CTkLabel(f, text=str(m['descricao'])[:35], width=240, anchor="w", font=("Arial", 12), text_color="black").grid(row=0, column=2)
            forma = str(m.get('forma', '')).replace("TRANSFERÊNCIA", "TRANSF.").upper()
            ctk.CTkLabel(f, text=forma, width=110, font=("Arial", 11, "bold"), text_color="#333333").grid(row=0, column=3)
            ctk.CTkLabel(f, text=f"R$ {float(m['valor']):.2f}", width=130, font=("Arial", 14, "bold"), text_color=txt_valor).grid(row=0, column=4)

        if not encontrou_algo:
            ctk.CTkLabel(self.scroll, text="Nenhuma movimentação registrada hoje.", text_color="gray").pack(pady=20)

    def atualizar_saldos(self):
        """ Atualiza os cards coloridos no topo com os valores do banco """
        for w in self.frame_cards.winfo_children(): w.destroy()
        
        # Busca os cálculos que fizemos no database.py
        res = database.calcular_resumo_caixa()
        
        cards = [
            ("SALDO TOTAL", res['total'], self.verde_medio), 
            ("SALDO DO DIA", res['dia'], self.laranja_busca), 
            ("APORTES", res['aportes'], "#4682B4")
        ]
        
        for tit, val, cor in cards:
            c = ctk.CTkFrame(self.frame_cards, fg_color=cor, width=250, height=95)
            c.pack(side="left", padx=10)
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=tit, text_color="white", font=("Arial", 12, "bold")).pack(pady=5)
            ctk.CTkLabel(c, text=f"R$ {val:,.2f}", text_color="white", font=("Arial", 20, "bold")).pack()

    def salvar_aporte(self):
        """ Coleta os dados da tela e envia para o banco de dados """
        desc = self.ent_desc.get().strip().upper()
        valor = self.ent_val.get().strip()
        
        if not desc or not valor:
            messagebox.showwarning("Aviso", "Preencha a Descrição e o Valor!")
            return
            
        # Monta o dicionário para o banco de dados
        dados = {
            "data": datetime.now().strftime("%d/%m/%Y"), 
            "desc": desc, 
            "tipo": "APORTE", 
            "cat": self.combo_cat.get(), 
            "valor": valor, 
            "forma": "APORTE"
        }
        
        if database.registrar_movimento_caixa(dados):
            messagebox.showinfo("Sucesso", "Movimentação lançada com sucesso!")
            # Limpa os campos para o próximo lançamento
            self.ent_desc.delete(0, 'end')
            self.ent_val.delete(0, 'end')
            # Atualiza os componentes da tela
            self.atualizar_saldos()
            self.renderizar_tabela()
        else:
            messagebox.showerror("Erro", "Falha ao gravar no banco de dados.")
