import customtkinter as ctk
import database
import os
from tkinter import messagebox
from datetime import datetime
from produtos import JanelaBusca 
from fpdf import FPDF

class JanelaQuantidade(ctk.CTkToplevel):
    """ Janela de diálogo personalizada em Branco e Verde """
    def __init__(self, item_nome, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("320x180")
        self.title("Alterar Quantidade")
        self.configure(fg_color="white") # FUNDO BRANCO
        self.resizable(False, False)
        self.result = None
        
        # Garante que a janela fique por cima e impeça cliques fora
        self.grab_set()

        ctk.CTkLabel(self, text=f"Nova quantidade para:\n{item_nome}", 
                     text_color="black", font=("Arial", 12, "bold")).pack(pady=15)
        
        # Entrada com borda VERDE e fundo BRANCO
        self.entry = ctk.CTkEntry(self, width=150, fg_color="white", border_color="#2E8B57", 
                                  text_color="black", font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.focus()

        # Botão VERDE conforme seu padrão
        btn = ctk.CTkButton(self, text="CONFIRMAR", fg_color="#2E8B57", hover_color="#145B06",
                            text_color="white", font=("Arial", 11, "bold"), command=self.confirmar)
        btn.pack(pady=15)

    def confirmar(self):
        self.result = self.entry.get()
        self.destroy()

    def obter_valor(self):
        self.master.wait_window(self)
        return self.result


class Orcamentos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.carrinho_produtos = []
        self.carrinho_servicos = []
        self.cliente_selecionado = None
        self.total_produtos = 0.0
        self.total_servicos = 0.0

    def abrir_orcamento(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        # --- CABEÇALHO ---
        header = ctk.CTkFrame(self, fg_color="#145B06", height=50, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="📑 NOVO ORÇAMENTO / O.S.", 
                     font=("Arial", 16, "bold"), text_color="white").pack(pady=12)

        # --- FRAME 1: DADOS DO CLIENTE ---
        self.frame_cliente = ctk.CTkFrame(self, fg_color="#F9F9F9", border_width=1, border_color="#E0E0E0")
        self.frame_cliente.pack(fill="x", padx=20, pady=10)

        self.tipo_cli_var = ctk.StringVar(value="pf")
        ctk.CTkRadioButton(self.frame_cliente, text="Pessoa Física", variable=self.tipo_cli_var, value="pf", 
                           text_color="black", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkRadioButton(self.frame_cliente, text="Pessoa Jurídica", variable=self.tipo_cli_var, value="pj", 
                           text_color="black", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)

        # Campo de Busca Cliente com fundo BRANCO e borda VERDE
        self.entry_busca_cli = ctk.CTkEntry(self.frame_cliente, placeholder_text="Nome ou CPF/CNPJ...", 
                                            width=200, fg_color="white", border_color="#2E8B57", text_color="black")
        self.entry_busca_cli.grid(row=0, column=2, padx=5)

        btn_busca_cli = ctk.CTkButton(self.frame_cliente, text="🔍 BUSCAR", width=80, fg_color="#D2691E", hover_color="#145B06"
                                      , command=self.buscar_cliente_orc)
        btn_busca_cli.grid(row=0, column=3, padx=5)

        self.label_dados_cli = ctk.CTkLabel(self.frame_cliente, text="Nenhum cliente selecionado", 
                                           font=("Arial", 12), text_color="black")
        self.label_dados_cli.grid(row=0, column=4, padx=20, sticky="w")

        # --- FRAME 2: SELEÇÃO DE ITENS (ESTILIZADO) ---
        self.frame_selecao = ctk.CTkFrame(self, fg_color="white") 
        self.frame_selecao.pack(fill="x", padx=20, pady=5)

        self.entry_filtro = ctk.CTkEntry(self.frame_selecao, placeholder_text="Filtrar produto/serviço...", 
                                         width=280, border_color="#2E8B57", fg_color="white", text_color="black")
        self.entry_filtro.grid(row=0, column=0, padx=5)

        ctk.CTkButton(self.frame_selecao, text="+ PRODUTO", fg_color="#2E8B57", hover_color="#145B06", width=110,
                      command=lambda: self.abrir_busca_item("produto")).grid(row=0, column=1, padx=5)

        ctk.CTkButton(self.frame_selecao, text="+ SERVIÇO", fg_color="#2E8B57", hover_color="#145B06", width=110,
                      command=lambda: self.abrir_busca_item("servico")).grid(row=0, column=2, padx=5)

        # Chamada para criar a tabela e rodapé (que estarão na Parte 2)
        self.configurar_tabela_e_rodape()

    # --- LÓGICA DE BUSCA DO CLIENTE FILTRADA ---
    def buscar_cliente_orc(self):
        tipo = self.tipo_cli_var.get()
        termo = self.entry_busca_cli.get() 
        if tipo == "pf":
            res = database.buscar_clientes_pf_flexivel(termo)
        else:
            res = database.buscar_clientes_pj_flexivel(termo)
        
        if res:
            from clientes import JanelaBuscaClientes
            JanelaBuscaClientes(res, self.set_cliente, tipo)
        else:
            messagebox.showinfo("Aviso", "Nenhum cliente encontrado.")

    def set_cliente(self, cliente):
        self.cliente_selecionado = cliente
        nome = cliente['nome'] if 'nome' in cliente else cliente['empresa']
        doc = cliente['cpf'] if 'cpf' in cliente else cliente['cnpj']
        endereco = f"{cliente['logradouro']}, {cliente['numero']} - {cliente['bairro']}"
        self.label_dados_cli.configure(text=f"✅ {nome} | {doc}\n📍 {endereco}", 
                                       text_color="#145B06", font=("Arial", 12, "bold"))

    def abrir_busca_item(self, tipo):
        termo = self.entry_filtro.get()
        res = database.buscar_produtos_flexivel(termo) if tipo == "produto" else database.buscar_servicos_flexivel(termo)
        if res:
            JanelaBusca(res, self.adicionar_item_carrinho, tipo)
        else:
            messagebox.showinfo("Busca", "Nenhum item encontrado.")
    # --- ETAPA 2: TABELA, EDIÇÃO E FINALIZAÇÃO ---

    def configurar_tabela_e_rodape(self):
        """ Cria a estrutura da tabela e o resumo financeiro """
        # Cabeçalho da Tabela (Verde Escuro)
        self.frame_lista_header = ctk.CTkFrame(self, fg_color="#145B06", height=30, corner_radius=5)
        self.frame_lista_header.pack(fill="x", padx=20, pady=(10,0))
        
        headers = [("DESCRIÇÃO", 300), ("QTD", 80), ("UNIT.", 100), ("TOTAL", 100), ("AÇÕES", 100)]
        for i, (txt, w) in enumerate(headers):
            ctk.CTkLabel(self.frame_lista_header, text=txt, width=w, font=("Arial", 11, "bold"), text_color="white").grid(row=0, column=i)

        # Área de Rolagem (Fundo Branco)
        self.scroll_itens = ctk.CTkScrollableFrame(self, fg_color="white", height=280, border_width=1, border_color="#E0E0E0")
        self.scroll_itens.pack(fill="both", expand=True, padx=20, pady=(0,5))

        # Rodapé Compacto
        self.frame_totais = ctk.CTkFrame(self, fg_color="#F9F9F9", height=50)
        self.frame_totais.pack(fill="x", padx=20, pady=10)

        self.label_total_resumo = ctk.CTkLabel(self.frame_totais, text="TOTAL GERAL: R$ 0,00",
                                              font=("Arial", 12, "bold"), text_color="#145B06")
        self.label_total_resumo.pack(side="left", padx=15)

        self.btn_finalizar = ctk.CTkButton(self.frame_totais, text="FINALIZAR", width=100, height=30,
                                           fg_color="#2E8B57", hover_color="#145B06", font=("Arial", 11, "bold"),
                                           command=self.finalizar_orcamento)
        self.btn_finalizar.pack(side="right", padx=15)

    def adicionar_item_carrinho(self, item):
        id_item = item['descricao'] if 'descricao' in item else f"{item['produto']} ({item['fabricante']})"
        
        # Garante a captura do ID, não importa se veio como 'id' ou outra chave
        id_banco = item.get('id') 
        
        valor_bruto = item['v_final'] if 'v_final' in item else item['v_venda']
        if isinstance(valor_bruto, str):
            valor_unit = float(valor_bruto.replace("R$", "").replace(".", "").replace(",", ".").strip())
        else:
            valor_unit = float(valor_bruto)
        
        for i in self.carrinho_produtos + self.carrinho_servicos:
            if i['identificador'] == id_item:
                i['qtd'] += 1
                i['total'] = i['qtd'] * i['valor']
                self.renderizar_itens(); return
        
        novo = {
            'id': id_banco, 
            'identificador': id_item, 
            'valor': valor_unit,
            'tipo': 'servico' if 'descricao' in item else 'produto',
            'qtd': 1, 
            'total': valor_unit
        }
        if novo['tipo'] == 'produto': self.carrinho_produtos.append(novo)
        else: self.carrinho_servicos.append(novo)
        self.renderizar_itens()



    def renderizar_itens(self):
        for widget in self.scroll_itens.winfo_children(): widget.destroy()
        self.total_produtos = 0.0; self.total_servicos = 0.0

        for item in self.carrinho_produtos + self.carrinho_servicos:
            linha = ctk.CTkFrame(self.scroll_itens, fg_color="transparent")
            linha.pack(fill="x", pady=2)

            # LETRAS EM PRETO PARA MÁXIMA VISIBILIDADE
            ctk.CTkLabel(linha, text=item['identificador'], width=300, anchor="w", text_color="black").grid(row=0, column=0, padx=5)
            ctk.CTkLabel(linha, text=str(item['qtd']), width=80, text_color="black").grid(row=0, column=1)
            ctk.CTkLabel(linha, text=f"R$ {item['valor']:.2f}", width=100, text_color="black").grid(row=0, column=2)
            ctk.CTkLabel(linha, text=f"R$ {item['total']:.2f}", width=100, font=("Arial", 11, "bold"), text_color="black").grid(row=0, column=3)

            # Botão EDITAR (Agora com texto claro e cor mais profissional)
            ctk.CTkButton(linha, text="EDITAR", width=50, height=25, 
                        fg_color="#2E8B57", # Azul escuro profissional
                        hover_color="#145B06",
                        font=("Arial", 10, "bold"),
                        command=lambda i=item: self.editar_quantidade(i)).grid(row=0, column=4, padx=2)

            # Botão EXCLUIR (Vermelho mais suave)
            ctk.CTkButton(linha, text="REMOVER", width=60, height=25, 
                        fg_color="#B22222", 
                        hover_color="#8B1A1A",
                        font=("Arial", 10, "bold"),
                        command=lambda i=item: self.remover_item(i)).grid(row=0, column=5, padx=2)


            if item['tipo'] == 'produto': self.total_produtos += item['total']
            else: self.total_servicos += item['total']

        total = self.total_produtos + self.total_servicos
        self.label_total_resumo.configure(text=f"Prod: R$ {self.total_produtos:.2f} | Serv: R$ {self.total_servicos:.2f} | TOTAL: R$ {total:.2f}")

    def editar_quantidade(self, item):
        # Chama a nova janela personalizada
        dialogo = JanelaQuantidade(item['identificador'], master=self)
        nova_qtd = dialogo.obter_valor()
        
        if nova_qtd:
            # Tratamento para aceitar vírgula (padrão brasileiro) e transformar em float
            try:
                valor_limpo = nova_qtd.replace(',', '.')
                qtd_float = float(valor_limpo)
                
                if qtd_float > 0:
                    item['qtd'] = qtd_float
                    item['total'] = item['qtd'] * item['valor']
                    self.renderizar_itens()
            except ValueError:
                messagebox.showwarning("Erro", "Digite um valor numérico válido.")


    def remover_item(self, item):
        if item in self.carrinho_produtos: self.carrinho_produtos.remove(item)
        else: self.carrinho_servicos.remove(item)
        self.renderizar_itens()

    def finalizar_orcamento(self):
        if not self.cliente_selecionado or not (self.carrinho_produtos + self.carrinho_servicos):
            return messagebox.showwarning("Aviso", "Selecione o cliente e adicione itens!")
        
        # 1. Coleta os dados para o Banco
        nome = self.cliente_selecionado['nome'] if 'nome' in self.cliente_selecionado else self.cliente_selecionado['empresa']
        doc = self.cliente_selecionado['cpf'] if 'cpf' in self.cliente_selecionado else self.cliente_selecionado['cnpj']
        
        dados_h = {
            'tipo_cliente': self.tipo_cli_var.get(),
            'cliente_id': self.cliente_selecionado['id'],
            'nome_cliente': nome,
            'documento': doc,
            'endereco_completo': f"{self.cliente_selecionado['logradouro']}, {self.cliente_selecionado['numero']}",
            'data_emissao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'validade_dias': 7,
            'total_produtos': self.total_produtos,
            'total_servicos': self.total_servicos,
            'valor_geral': self.total_produtos + self.total_servicos,
            'status': 'Pendente'
        }

        # 2. Chama a gravação no banco e gera o PDF
        try:
            # Tenta salvar no database.py
            sucesso = database.salvar_orcamento_completo(dados_h, self.carrinho_produtos + self.carrinho_servicos)
            
            if sucesso:
                # Se salvou, gera o PDF usando os dados coletados
                self.gerar_pdf_orcamento(dados_h)
                messagebox.showinfo("Sucesso", "Orçamento finalizado e PDF gerado!")
                self.resetar_tela()
            else:
                messagebox.showerror("Erro", "Falha ao gravar no banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


    def gerar_pdf_orcamento(self, dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Cabeçalho do PDF
        pdf.cell(190, 8, f"Data: {dados['data_emissao']}", ln=True)
        pdf.ln(10)
        
               # --- Dados do Cliente (CORRIGIDO) ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 8, f"Cliente: {dados['nome_cliente']}", ln=True)
        pdf.cell(190, 8, f"Documento: {dados['documento']}", ln=True)
        # Aqui estava o erro: trocamos ['data'] por ['data_emissao']
        pdf.cell(190, 8, f"Data: {dados['data_emissao']}", ln=True) 
        pdf.ln(5)

        
        # Tabela de Itens
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(100, 10, "Item", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Qtd", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Unit.", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Total", 1, 1, 'C', 1)
        
        pdf.set_font("Arial", '', 10)
        for item in self.carrinho_produtos + self.carrinho_servicos:
            pdf.cell(100, 8, str(item['identificador']), 1)
            pdf.cell(30, 8, str(item['qtd']), 1, 0, 'C')
            pdf.cell(30, 8, f"R$ {item['valor']:.2f}", 1, 0, 'R')
            pdf.cell(30, 8, f"R$ {item['total']:.2f}", 1, 1, 'R')
            
        # Total Final
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, f"TOTAL GERAL: R$ {dados['valor_geral']:.2f}", ln=True, align='R')
        
        # Salva e abre o arquivo
        nome_arquivo = f"Orcamento_{datetime.now().strftime('%H%M%S')}.pdf"
        pdf.output(nome_arquivo)
        os.startfile(nome_arquivo)

    def resetar_tela(self):
        self.cliente_selecionado = None
        self.carrinho_produtos = []
        self.carrinho_servicos = []
        self.label_dados_cli.configure(text="Nenhum cliente selecionado", text_color="black")
        self.renderizar_itens()
