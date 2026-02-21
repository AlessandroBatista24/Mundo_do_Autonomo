import customtkinter as ctk
import database
from tkinter import messagebox
from datetime import datetime
import os

class Relatorios(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.verde_escuro = "#145B06"
        self.verde_medio = "#2E8B57"
        self.laranja_busca = "#D2691E"
        self.cinza_fundo = "#F9F9F9"
        
    def abrir_relatorios(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        header = ctk.CTkFrame(self, fg_color=self.verde_escuro, height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="📊 CENTRO DE RELATÓRIOS E HISTÓRICO", 
                     font=("Arial", 18, "bold"), text_color="white").pack(pady=15)

        self.frame_filtros = ctk.CTkFrame(self, fg_color=self.cinza_fundo, border_width=1, border_color="#E0E0E0")
        self.frame_filtros.pack(fill="x", padx=20, pady=10)

        # 1. Relatório de (Com as cores restauradas)
        ctk.CTkLabel(self.frame_filtros, text="Relatório de:", text_color="black", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.combo_tipo = ctk.CTkComboBox(self.frame_filtros, values=["Histórico de O.S.", "Contas Pagas", "Contas Recebidas", "Caixa / Movimentação"], 
                                         width=150, fg_color="white", border_color=self.verde_medio, button_color=self.verde_medio,
                                         text_color="black", dropdown_fg_color="white", dropdown_text_color="black", dropdown_hover_color="#98FB98")
        self.combo_tipo.grid(row=1, column=0, padx=5, pady=(0,15))

        # 2. Período (Com as cores restauradas)
        ctk.CTkLabel(self.frame_filtros, text="Período:", text_color="black", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=5, pady=5)
        self.combo_per = ctk.CTkComboBox(self.frame_filtros, values=["Geral", "Diário", "Mensal", "Anual"], 
                                        width=100, fg_color="white", border_color=self.verde_medio, button_color=self.verde_medio,
                                        text_color="black", dropdown_fg_color="white", dropdown_text_color="black", dropdown_hover_color="#98FB98")
        self.combo_per.grid(row=1, column=1, padx=5, pady=(0,15))

        # 3. Busca
        ctk.CTkLabel(self.frame_filtros, text="Busca / Data Ref:", text_color="black", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5, pady=5)
        
        self.ent_ref = ctk.CTkEntry(self.frame_filtros, 
                                    placeholder_text="01/02/2026 ou 02/2026", # <-- Texto de instrução aqui
                                    width=160, # Aumentei um pouco para lerem melhor a instrução
                                    fg_color="white", 
                                    border_color=self.verde_medio, 
                                    text_color="black",
                                    placeholder_text_color="gray") # Cor cinza para a instrução
        self.ent_ref.grid(row=1, column=2, padx=5, pady=(0,15))

        
        # 4. Botão Buscar
        ctk.CTkButton(self.frame_filtros, text="🔍 BUSCAR", width=90, fg_color=self.laranja_busca, 
                      hover_color=self.verde_escuro, font=("Arial", 11, "bold"), 
                      command=self.processar_relatorio).grid(row=1, column=3, padx=5, pady=(0,15))

        # 5. Botão Imprimir
        ctk.CTkButton(self.frame_filtros, text="🖨️ IMPRIMIR PDF", width=110, fg_color=self.verde_medio, 
                      hover_color=self.verde_escuro, font=("Arial", 11, "bold"), 
                      command=self.gerar_pdf_financeiro).grid(row=1, column=4, padx=5, pady=(0,15))

        # --- AQUI ESTÁ O QUE TINHA SUMIDO: OS CÁLCULOS ---
        self.frame_resumo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_resumo.pack(fill="x", padx=10, pady=5)
        
        # ESSA LINHA ABAIXO É O QUE FAZ OS CARDS APARECEREM NA ABERTURA
        self.atualizar_cards(0, 0)

        self.scroll_res = ctk.CTkScrollableFrame(self, fg_color="white", border_width=1, border_color="#E0E0E0")
        self.scroll_res.pack(fill="both", expand=True, padx=20, pady=10)


    def atualizar_cards(self, ent, sai):
        for w in self.frame_resumo.winfo_children(): w.destroy()
        saldo = ent - sai
        cards = [("ENTRADAS", f"R$ {ent:,.2f}", self.verde_medio), 
                 ("SAÍDAS", f"R$ {sai:,.2f}", "#B22222"), 
                 ("SALDO LÍQUIDO", f"R$ {saldo:,.2f}", "#4682B4")]
        for t, v, c in cards:
            f = ctk.CTkFrame(self.frame_resumo, fg_color=c, width=280, height=80)
            f.pack(side="left", padx=10, expand=True); f.pack_propagate(False)
            ctk.CTkLabel(f, text=t, text_color="white", font=("Arial", 11, "bold")).pack(pady=5)
            ctk.CTkLabel(f, text=v, text_color="white", font=("Arial", 18, "bold")).pack()

    def processar_relatorio(self):
        for w in self.scroll_res.winfo_children(): w.destroy()
        tipo = self.combo_tipo.get()
        periodo = self.combo_per.get()
        ref = self.ent_ref.get().strip() # Limpa espaços extras

        # Captura de datas para o banco
        d_ini, d_fim = None, None
        
        # Se for DIÁRIO, a data de início é a referência digitada
        if periodo == "Diário" and ref:
            d_ini = ref
            d_fim = ref
        
        # Chamada das funções do banco
        if tipo == "Histórico de O.S.":
            dados = database.buscar_os_fechadas(ref)
            self.renderizar_os(dados)
            return

        if tipo == "Contas Pagas":
            lista = database.buscar_historico_pagar(ref)
        elif tipo == "Contas Recebidas":
            lista = database.buscar_historico_receber(ref)
        else:
            # PARA O CAIXA: Passamos as datas para a função que corrigimos no database.py
            lista = database.buscar_extrato_caixa(filtro=ref, data_inicio=d_ini, data_fim=d_fim)
        
        # Exibe na tela (o filtro visual do Python serve como segunda camada de segurança)
        self.filtrar_e_exibir_financeiro(lista, periodo, ref)



    def filtrar_e_exibir_financeiro(self, lista, periodo, ref):
        ent, sai = 0.0, 0.0
        encontrou_algo = False
        ref_limpa = ref.strip() # Remove espaços invisíveis da busca

        for item in lista:
            # Captura a data de qualquer tabela de forma segura
            data_item = str(item.get('data') or item.get('data_movimento') or \
                        item.get('data_pagamento') or item.get('data_recebimento') or "").strip()
            
            if not data_item: continue 
            
            mostrar = False
            
            # --- LÓGICA DE FILTRO CORRIGIDA (2026) ---
            if not ref_limpa or periodo == "Geral":
                mostrar = True # Se não digitar nada, mostra tudo
            
            # Se você digitou algo, verificamos se o texto está CONTIDO na data
            elif ref_limpa in data_item:
                mostrar = True

            if mostrar:
                encontrou_algo = True
                # Captura valor (qualquer coluna de valor que existir)
                valor = float(item.get('valor') or item.get('valor_pago') or \
                              item.get('valor_recebido') or item.get('valor_total') or 0)
                
                # Identifica Entrada ou Saída para os CARDS
                e_saida = any(k in item for k in ['credor', 'id_conta', 'valor_pago']) or \
                          item.get('tipo') == 'SAIDA'
                
                if e_saida:
                    sai += valor
                else:
                    ent += valor
                
                origem = item.get('cliente') or item.get('credor') or \
                         item.get('origem') or item.get('descricao') or "Sem descrição"
                
                self.criar_linha_financeira(data_item, origem, valor)
        
        # ATUALIZA OS CARDS (ENTRADAS / SAÍDAS)
        self.atualizar_cards(ent, sai)
        
        if not encontrou_algo:
            ctk.CTkLabel(self.scroll_res, text=f"Nenhum registro encontrado para: {ref_limpa}", 
                         text_color="gray").pack(pady=20)


    def criar_linha_financeira(self, data, desc, valor):
        """ Desenha cada linha de resultado no scrollable frame """
        f = ctk.CTkFrame(self.scroll_res, fg_color=self.cinza_fundo, height=35)
        f.pack(fill="x", pady=1); f.pack_propagate(False)
        ctk.CTkLabel(f, text=f"{data} | {str(desc)[:40]} | R$ {valor:.2f}", text_color="black").pack(side="left", padx=10)

    def renderizar_os(self, lista):
        """ Renderiza a lista de O.S. para reimpressão """
        self.atualizar_cards(0, 0)
        if not lista:
            ctk.CTkLabel(self.scroll_res, text="Nenhuma O.S. encontrada.", text_color="gray").pack(pady=20)
            return
        for os_data in lista:
            f = ctk.CTkFrame(self.scroll_res, fg_color=self.cinza_fundo, height=50, border_width=1, border_color="#E0E0E0")
            f.pack(fill="x", pady=2); f.pack_propagate(False)
            info = f"O.S. Nº {os_data['id_os']} | Cliente: {os_data['nome_cliente']} | Total: R$ {os_data['valor_geral']:.2f}"
            ctk.CTkLabel(f, text=info, text_color="black", font=("Arial", 12, "bold")).pack(side="left", padx=15)
            ctk.CTkButton(f, text="🖨️ REIMPRIMIR", width=110, height=30, fg_color=self.verde_medio,
                          command=lambda d=os_data: self.reimprimir_pdf(d)).pack(side="right", padx=10)

    def reimprimir_pdf(self, dados_os):
        try:
            # 1. Garante que o ID existe (seja id_os ou id_orcamento)
            id_atual = dados_os.get('id_os') or dados_os.get('id_orcamento')
            
            # 2. "VACINA" contra o erro: se o gerador de PDF pede 'id_orcamento',
            # nós criamos essa chave no dicionário antes de enviar
            dados_copia = dados_os.copy()
            if 'id_orcamento' not in dados_copia:
                dados_copia['id_orcamento'] = id_atual

            # 3. Busca os itens usando o ID correto do banco
            itens = database.buscar_itens_da_os(id_atual) 
            
            # 4. Importa e gera o PDF usando a cópia "vacinada"
            from os_modulo import OS
            gerador = OS(self.master)
            gerador.gerar_pdf_os(dados_copia, itens)
            
        except Exception as e:
            messagebox.showerror("Erro de Impressão", f"Detalhe do erro: {e}")

    def gerar_pdf_financeiro(self):
        try:
            from fpdf import FPDF
            import os
            
            tipo = self.combo_tipo.get()
            periodo = self.combo_per.get()
            ref = self.ent_ref.get()

            # 1. Configuração do PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", "B", 16)
            pdf.cell(190, 10, f"RELATORIO: {tipo.upper()}", ln=True, align="C")
            pdf.set_font("helvetica", "", 12)
            pdf.cell(190, 10, f"Periodo: {periodo} | Ref: {ref if ref else 'Geral'}", ln=True, align="C")
            pdf.ln(10)

            # 2. Cabeçalho da Tabela
            pdf.set_fill_color(20, 91, 6) # Seu Verde Escuro (#145B06)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(30, 8, "DATA", 1, 0, "C", True)
            pdf.cell(110, 8, "DESCRICAO / ORIGEM", 1, 0, "L", True)
            pdf.cell(50, 8, "VALOR (R$)", 1, 1, "R", True)

            # 3. Busca de Dados (Mesma lógica da tela)
            if tipo == "Contas Pagas": lista = database.buscar_historico_pagar(ref)
            elif tipo == "Contas Recebidas": lista = database.buscar_historico_receber(ref)
            else: lista = database.buscar_extrato_caixa(ref)

            pdf.set_text_color(0, 0, 0)
            pdf.set_font("helvetica", "", 10)
            total_geral = 0.0
            cont = 0

            for item in lista:
                # Captura data e valor de forma blindada
                dt = item.get('data') or item.get('data_pagamento') or item.get('data_recebimento') or item.get('data_movimento') or item.get('data_vencimento')
                vl = float(item.get('valor') or item.get('valor_pago') or item.get('valor_recebido') or item.get('valor_total') or 0)
                desc = str(item.get('cliente') or item.get('credor') or item.get('origem') or item.get('descricao'))[:55]

                # Filtro de exibição (Igual ao da tela)
                mostrar = False
                if periodo == "Geral": mostrar = True
                elif ref in str(dt): mostrar = True

                if mostrar:
                    # Zebra na tabela (cor sim, cor não)
                    bg = 245 if cont % 2 == 0 else 255
                    pdf.set_fill_color(bg, bg, bg)
                    pdf.cell(30, 8, str(dt), 1, 0, "C", True)
                    pdf.cell(110, 8, desc, 1, 0, "L", True)
                    pdf.cell(50, 8, f"{vl:.2f}", 1, 1, "R", True)
                    total_geral += vl
                    cont += 1

            # 4. Rodapé Financeiro
            pdf.ln(5)
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(140, 10, "TOTAL DO PERIODO:", 0, 0, "R")
            pdf.set_text_color(20, 91, 6)
            pdf.cell(50, 10, f"R$ {total_geral:.2f}", 0, 1, "R")

            # 5. Salvar e abrir o arquivo
            nome_limpo = tipo.replace(' ', '_').replace('/', '-')
            nome_arq = f"Relatorio_{nome_limpo}.pdf"
            
            pdf.output(nome_arq)
            os.startfile(nome_arq)

        except Exception as e:
            messagebox.showerror("Erro na Impressão", f"Não foi possível gerar o PDF: {e}")
