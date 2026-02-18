import customtkinter as ctk
import database
from tkinter import messagebox
from fpdf import FPDF
import os
from datetime import datetime

class OS(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def abrir_os(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        header = ctk.CTkFrame(self, fg_color="#145B06", height=50, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="🛠️ GESTÃO DE ORDENS DE SERVIÇO", 
                     font=("Arial", 16, "bold"), text_color="white").pack(pady=12)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)

        self.entry_busca = ctk.CTkEntry(search_frame, placeholder_text="Buscar orçamento pendente...", 
                                        width=400, border_color="#2E8B57", fg_color="white", text_color="black")
        self.entry_busca.pack(side="left", padx=5)
        self.entry_busca.bind("<Return>", lambda e: self.listar_pendentes())

        ctk.CTkButton(search_frame, text="🔍 ATUALIZAR", width=100, fg_color="#D2691E", hover_color="#145B06", command=self.listar_pendentes).pack(side="left", padx=5)

        self.scroll_lista = ctk.CTkScrollableFrame(self, fg_color="white", border_width=1, border_color="#E0E0E0")
        self.scroll_lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.listar_pendentes()

    def listar_pendentes(self):
        for widget in self.scroll_lista.winfo_children(): widget.destroy()
        termo = self.entry_busca.get()
        orcamentos = database.buscar_orcamentos_pendentes(termo)

        if not orcamentos:
            ctk.CTkLabel(self.scroll_lista, text="Nenhum orçamento pendente.", text_color="gray").pack(pady=40)
            return

        for orc in orcamentos:
            linha = ctk.CTkFrame(self.scroll_lista, fg_color="#F9F9F9", border_width=1, border_color="#E8E8E8")
            linha.pack(fill="x", pady=3, padx=5)

            info = f"ID: {orc['id_orcamento']} | Cliente: {orc['nome_cliente']} | Total: R$ {orc['valor_geral']:.2f}"
            ctk.CTkLabel(linha, text=info, text_color="black", font=("Arial", 12, "bold")).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(linha, text="EXCLUIR", width=80, fg_color="#B22222", hover_color="#145B06", 
                          command=lambda o=orc: self.confirmar_recusa(o)).pack(side="right", padx=10)
            ctk.CTkButton(linha, text="APROVAR O.S.", width=110, fg_color="#2E8B57", hover_color="#145B06",
                          command=lambda o=orc: self.confirmar_aprovacao(o)).pack(side="right", padx=5)

    def confirmar_aprovacao(self, orc):
        if messagebox.askyesno("Aprovar", f"Converter orçamento {orc['id_orcamento']} em O.S.?"):
            # Buscamos os itens DETALHADOS antes da conversão
            itens_pdf = database.buscar_itens_do_orcamento(orc['id_orcamento'])
            
            if database.aprovar_e_converter_orcamento(orc['id_orcamento']):
                self.gerar_pdf_os(orc, itens_pdf)
                messagebox.showinfo("Sucesso", "Ordem de Serviço gerada!")
                self.listar_pendentes()

    def confirmar_recusa(self, orc):
        if messagebox.askyesno("Excluir", "Deseja deletar este orçamento?"):
            if database.excluir_orcamento_recusado(orc['id_orcamento']):
                self.listar_pendentes()

    def gerar_pdf_os(self, dados, itens):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.set_fill_color(20, 91, 6); pdf.set_text_color(255, 255, 255)
        pdf.cell(190, 15, f"ORDEM DE SERVIÇO Nº {dados['id_orcamento']}", 1, 1, 'C', 1)
        
        pdf.ln(5); pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", 'B', 11)
        pdf.cell(100, 8, f"CLIENTE: {dados['nome_cliente']}", 0, 0)
        pdf.cell(90, 8, f"DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.cell(100, 8, f"DOCUMENTO: {dados['documento']}", 0, 1)
        
        pdf.ln(5)
        pdf.set_fill_color(230, 230, 230); pdf.set_font("Arial", 'B', 10)
        pdf.cell(110, 10, "DESCRIÇÃO DO ITEM", 1, 0, 'C', 1)
        pdf.cell(20, 10, "QTD", 1, 0, 'C', 1)
        pdf.cell(30, 10, "UNIT.", 1, 0, 'C', 1)
        pdf.cell(30, 10, "TOTAL", 1, 1, 'C', 1)
        
        pdf.set_font("Arial", '', 9)
        for item in itens:
            pdf.cell(110, 8, str(item['nome_item']), 1)
            pdf.cell(20, 8, str(item['quantidade']), 1, 0, 'C')
            pdf.cell(30, 8, f"R$ {item['valor_unitario']:.2f}", 1, 0, 'R')
            pdf.cell(30, 8, f"R$ {item['valor_total_item']:.2f}", 1, 1, 'R')
            
        pdf.ln(5); pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, f"VALOR TOTAL: R$ {dados['valor_geral']:.2f}", 0, 1, 'R')

        pdf.ln(10); pdf.set_font("Arial", 'B', 10); pdf.cell(190, 8, "LAUDO TÉCNICO / OBSERVAÇÕES:", 0, 1)
        pdf.rect(10, pdf.get_y(), 190, 35) 
        
        pdf.ln(45)
        pdf.cell(85, 0.1, "", 1, 0); pdf.cell(20, 0.1, "", 0, 0); pdf.cell(85, 0.1, "", 1, 1)
        pdf.cell(85, 8, "Responsável Técnico", 0, 0, 'C')
        pdf.cell(20, 8, "", 0, 0); pdf.cell(85, 8, "Assinatura do Cliente", 0, 1, 'C')

        nome = f"OS_Final_{dados['id_orcamento']}.pdf"
        pdf.output(nome); os.startfile(nome)
