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
        ctk.CTkLabel(header, text="💰 FLUXO DE CAIXA E APORTES", 
                     font=("Arial", 20, "bold"), text_color="white").pack(pady=15)

        # --- DASHBOARD (CARDS) ---
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent", height=110)
        self.frame_cards.pack(fill="x", padx=20, pady=10)
        self.frame_cards.pack_propagate(False)
        self.atualizar_saldos()

        # --- ÁREA DE LANÇAMENTO ---
        self.frame_add = ctk.CTkFrame(self, fg_color=self.cinza_fundo, border_width=1, border_color=self.borda_cinza)
        self.frame_add.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.frame_add, text="Descrição:", font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        self.ent_desc = ctk.CTkEntry(self.frame_add, width=220, height=35, fg_color="white", border_color=self.verde_medio, text_color="black")
        self.ent_desc.grid(row=1, column=0, padx=10, pady=(0,10))

        ctk.CTkLabel(self.frame_add, text="Tipo:", font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=1, padx=10, pady=(5,0), sticky="w")
        self.combo_cat = ctk.CTkComboBox(self.frame_add, values=["INICIAL", "EMPR.", "INVEST."], 
                                         width=140, height=35, fg_color="white", border_color=self.verde_medio, 
                                         button_color=self.verde_medio, text_color="black")
        self.combo_cat.set("INVEST.")
        self.combo_cat.grid(row=1, column=1, padx=10, pady=(0,10))

        ctk.CTkLabel(self.frame_add, text="Valor R$:", font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=2, padx=10, pady=(5,0), sticky="w")
        self.ent_val = ctk.CTkEntry(self.frame_add, width=120, height=35, fg_color="white", border_color=self.verde_medio, text_color="black", font=("Arial", 14, "bold"))
        self.ent_val.grid(row=1, column=2, padx=10, pady=(0,10))

        self.btn_lancar = ctk.CTkButton(self.frame_add, text="LANÇAR", fg_color=self.verde_medio, 
                                        hover_color=self.verde_escuro, font=("Arial", 12, "bold"), height=35, command=self.salvar_aporte)
        self.btn_lancar.grid(row=1, column=3, padx=20, pady=(0,10))

                # --- FILTROS (AJUSTADOS PARA BRANCO) ---
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(fill="x", padx=20, pady=10)
        
        # Campo de Busca Geral
        self.ent_busca = ctk.CTkEntry(self.frame_filtros, placeholder_text="Filtrar...", 
                                      width=230, height=32, fg_color="white", 
                                      border_color=self.verde_medio, text_color="black")
        self.ent_busca.grid(row=0, column=0, padx=5)
        self.ent_busca.bind("<KeyRelease>", lambda e: self.renderizar_tabela())
        
        # Campo Data Início
        self.ent_ini = ctk.CTkEntry(self.frame_filtros, placeholder_text="DD/MM/AAAA", 
                                    width=130, height=32, fg_color="white", 
                                    border_color=self.verde_medio, text_color="black")
        self.ent_ini.grid(row=0, column=1, padx=5)
        
        # Campo Data Fim
        self.ent_fim = ctk.CTkEntry(self.frame_filtros, placeholder_text="DD/MM/AAAA", 
                                    width=130, height=32, fg_color="white", 
                                    border_color=self.verde_medio, text_color="black")
        self.ent_fim.grid(row=0, column=2, padx=5)
        
        # Botão de Filtrar
        ctk.CTkButton(self.frame_filtros, text="FILTRAR DATA", fg_color=self.laranja_busca, 
                      hover_color=self.verde_escuro, font=("Arial", 11, "bold"), 
                      height=32, command=self.renderizar_tabela).grid(row=0, column=3, padx=5)


        # --- CABEÇALHO DA TABELA (RESTAURADO) ---
        self.frame_label_tabela = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=35, corner_radius=5)
        self.frame_label_tabela.pack(fill="x", padx=20, pady=(10,0))
        
        titulos = [("DATA", 90), ("ORIGEM", 140), ("DESCRIÇÃO", 260), ("FORMA", 110), ("VALOR", 130)]
        for i, (txt, w) in enumerate(titulos):
            ctk.CTkLabel(self.frame_label_tabela, text=txt, width=w, font=("Arial", 11, "bold"), text_color="white").grid(row=0, column=i)

        # --- EXTRATO ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="white", border_width=1, border_color=self.borda_cinza)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0,15))
        self.renderizar_tabela()

    def atualizar_saldos(self):
        for w in self.frame_cards.winfo_children(): w.destroy()
        res = database.calcular_resumo_caixa()
        cards = [("SALDO TOTAL", res['total'], self.verde_medio), ("SALDO DO DIA", res['dia'], self.laranja_busca), ("APORTES", res['aportes'], "#4682B4")]
        for tit, val, cor in cards:
            c = ctk.CTkFrame(self.frame_cards, fg_color=cor, width=250, height=95)
            c.pack(side="left", padx=10); c.pack_propagate(False)
            ctk.CTkLabel(c, text=tit, text_color="white", font=("Arial", 12, "bold")).pack(pady=5)
            ctk.CTkLabel(c, text=f"R$ {val:,.2f}", text_color="white", font=("Arial", 20, "bold")).pack()

    def salvar_aporte(self):
        if not self.ent_desc.get() or not self.ent_val.get(): return
        dados = {"data": datetime.now().strftime("%d/%m/%Y"), "desc": self.ent_desc.get().upper(), "tipo": "APORTE", "cat": self.combo_cat.get(), "valor": self.ent_val.get(), "forma": "TRANSF."}
        if database.registrar_movimento_caixa(dados):
            messagebox.showinfo("Sucesso", "Lançado!"); self.ent_desc.delete(0, 'end'); self.ent_val.delete(0, 'end')
            self.atualizar_saldos(); self.renderizar_tabela()

    def renderizar_tabela(self):
        for w in self.scroll.winfo_children(): w.destroy()
        movs = database.buscar_extrato_caixa(self.ent_busca.get(), self.ent_ini.get(), self.ent_fim.get())
        for m in movs:
            bg = self.cor_destaque_aporte if m['tipo'] == 'APORTE' else "white"
            txt_valor = "#145B06" if m['tipo'] in ['ENTRADA', 'APORTE'] else "#B22222"
            
            # --- LÓGICA DE ABREVIAÇÃO ---
            forma_limpa = str(m['forma']).upper()
            forma_limpa = forma_limpa.replace("TRANSFERÊNCIA", "TRANSF.").replace("ENTRADA MANUAL", "MANUAL")
            
            f = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=0, height=45)
            f.pack(fill="x", pady=2)
            f.pack_propagate(False)
            
            ctk.CTkLabel(f, text=m['data'], width=90, font=("Arial", 13), text_color="black").grid(row=0, column=0, pady=8)
            ctk.CTkLabel(f, text=m['origem'][:15], width=140, anchor="w", font=("Arial", 13, "bold"), text_color="black").grid(row=0, column=1)
            ctk.CTkLabel(f, text=m['descricao'][:35], width=260, anchor="w", font=("Arial", 13), text_color="black").grid(row=0, column=2)
            
            # Coluna Forma de Pagamento com texto grande e abreviado
            ctk.CTkLabel(f, text=forma_limpa, width=110, font=("Arial", 13, "bold"), text_color="#333333").grid(row=0, column=3)
            
            ctk.CTkLabel(f, text=f"R$ {float(m['valor']):.2f}", width=130, font=("Arial", 14, "bold"), text_color=txt_valor).grid(row=0, column=4)
