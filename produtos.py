import customtkinter as ctk  # Importa a biblioteca de interface moderna (CustomTkinter)
import database            # Importa o seu arquivo/módulo que lida com o Banco de Dados
from tkinter import messagebox  # Importa o componente para exibir avisos e erros

# --- JANELA DE SELEÇÃO PADRONIZADA (BRANCO E VERDE) ---
# Esta classe cria uma nova janela (Pop-up) para mostrar os resultados de uma pesquisa
class JanelaBusca(ctk.CTkToplevel):
    def __init__(self, resultados, callback, tipo="produto"):
        super().__init__()
        self.title("🔍 Selecionar Item")  # Define o título da janela pop-up
        self.geometry("550x450")          # Define o tamanho (Largura x Altura)
        self.configure(fg_color="white")  # Define a cor de fundo da janela como branco
        self.attributes("-topmost", True) # Faz a janela ficar sempre por cima das outras
        self.grab_set()                   # Bloqueia cliques na janela de trás até que esta feche
        self.callback = callback          # Armazena a função que devolverá o item escolhido

        # Cabeçalho Verde Escuro - Cria uma faixa colorida no topo
        header = ctk.CTkFrame(self, fg_color="#145B06", height=50, corner_radius=0)
        header.pack(fill="x") # Faz a faixa ocupar toda a largura horizontal
        
        # Texto dentro do cabeçalho
        ctk.CTkLabel(header, text="RESULTADOS ENCONTRADOS", font=("Arial", 16, "bold"), text_color="white").pack(pady=12)

        # Scrollbar (Moldura com Rolagem) - Onde os resultados aparecerão
        self.scroll = ctk.CTkScrollableFrame(self, width=500, height=320, fg_color="white", 
                                            scrollbar_button_color="#2E8B57", 
                                            scrollbar_button_hover_color="#1E5D3A")
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # Loop que percorre a lista de dicionários vinda do banco de dados
        for item in resultados:
            # Lógica para decidir o que escrever no card dependendo se for Produto ou Serviço
            if tipo == "produto":
                t_principal = f"📦 {item['produto']}"
                t_secundario = f"Fabricante: {item['fabricante']} | Qtd: {item['quantidade']}"
            else:
                t_principal = f"🛠️ {item['descricao']}"
                t_secundario = f"Preço Final: R$ {item['v_final']:.2f}"

            # Card (Moldura individual) para cada item da lista
            card = ctk.CTkFrame(self.scroll, fg_color="#F9F9F9", border_width=1, border_color="#E0E0E0")
            card.pack(fill="x", pady=3, padx=5)

            # Texto do nome do item (em negrito e verde)
            ctk.CTkLabel(card, text=t_principal, font=("Arial", 14, "bold"), text_color="#145B06").pack(anchor="w", padx=10, pady=(5,0))
            
            # Texto de detalhes (em cinza)
            ctk.CTkLabel(card, text=t_secundario, font=("Arial", 11), text_color="#555555").pack(anchor="w", padx=10, pady=(0,5))

            # Botão Selecionar dentro do card
            # O "lambda i=item" serve para "congelar" o valor de 'item' naquele botão específico
            btn = ctk.CTkButton(card, text="SELECIONAR", width=100, height=25, font=("Arial", 11, "bold"),
                                fg_color="#2E8B57", hover_color="#1E5D3A",
                                command=lambda i=item: self.selecionar(i))
            # Posicionamento absoluto do botão no lado direito do card
            btn.place(relx=0.97, rely=0.5, anchor="e")

    # Método que finaliza a escolha
    def selecionar(self, item):
        self.callback(item) # Executa a função da tela anterior passando o item escolhido
        self.destroy()      # Fecha a janela de busca

class Produtos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}
        self.id_original = None
        self.modo_edicao = False

    def abrir_produtos(self):
        """ Cria a interface de produtos com cabeçalho padronizado e largura total """
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")
        
        # --- ESSENCIAL: Configura a coluna para expandir e preencher o espaço ---
        self.grid_columnconfigure(1, weight=1)

        # --- CABEÇALHO COM LARGURA TOTAL (sticky="ew" e SEM padx) ---
        header = ctk.CTkFrame(self, fg_color="#145B06", height=50, corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew") # Removido padx daqui
        header.grid_propagate(False)
        
        ctk.CTkLabel(header, text="📦 CADASTRO DE PRODUTOS", 
                     font=("Arial", 16, "bold"), text_color="white").pack(pady=12)

         # Espaçador entre header e campos
        ctk.CTkLabel(self, text="", height=1).grid(row=1, column=0)
        
        campos = [
            ("Produto:", "produto", "Nome...", "entry", self.aplicar_titulo),
            ("Fabricante:", "fabricante", "Fabricante...", "entry", self.aplicar_titulo),
            ("Valor Compra:", "v_compra", "0.00", "entry", None),
            ("Custo Fixo (%):", "custo_fixo", "0", "entry", None),
            ("Imposto (%):", "imposto", "0", "entry", None),
            ("Margem Lucro (%):", "margem_lucro", "0", "entry", None),
            ("Quantidade:", "quantidade", "0", "entry", None),
            ("Unidade:", "unidade", ["UN", "MT", "RL", "CX", "KG"], "combo", None),
            ("Venda Final:", "v_venda", "R$ 0,00", "entry", None)
        ]

        # Loop de campos (Começando na row 2)
        for i, (txt, chave, msg, tipo, func) in enumerate(campos):
            ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06").grid(row=i+2, column=0, padx=25, pady=3, sticky="w")
            
            if tipo == "entry":
                widget = ctk.CTkEntry(self, width=400, height=35, placeholder_text=msg, fg_color="#F0F0F0", border_width=0, corner_radius=50, text_color="black")
                if chave == "v_venda": widget.configure(state="readonly", fg_color="#E0E0E0")
                if func: widget.bind("<KeyRelease>", lambda event, e=widget, f=func: f(e))
                if chave in ["v_compra", "imposto", "custo_fixo", "margem_lucro"]:
                    widget.bind("<KeyRelease>", lambda e: self.calcular_venda(), add="+")
            else:
                widget = ctk.CTkComboBox(self, width=400, height=35, values=msg, 
                                         fg_color="#E9F0EA",          
                                         button_color="#1E5D3A", 
                                         button_hover_color="#145B06",
                                         border_width=0, corner_radius=50, text_color="black",
                                         dropdown_fg_color="#2E8B57", dropdown_text_color="black")
            
            widget.grid(row=i+2, column=1, padx=5, pady=3, sticky="w")
            self.inputs[chave] = widget

        # --- BOTÕES REPOSICIONADOS ---
        y_btn = 460
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", width=120, height=35, fg_color="#2E8B57", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.fluxo_salvamento)
        self.btn_salvar.place(x=150, y=y_btn)
        
        self.btn_buscar = ctk.CTkButton(self, text="BUSCAR", width=120, height=35, fg_color="#D2691E", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.iniciar_busca)
        self.btn_buscar.place(x=300, y=y_btn)
        
        self.btn_retornar = ctk.CTkButton(self, text="RETORNAR", width=120, height=35, fg_color="#696969", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.resetar_interface)
        
        self.btn_deletar = ctk.CTkButton(self, text="DELETAR", width=120, height=35, fg_color="#B22222", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.excluir_produto)

    def aplicar_titulo(self, e):
        t = e.get().title(); p = e.index("insert"); e.delete(0, "end"); e.insert(0, t); e.icursor(p)

    def calcular_venda(self):
        try:
            compra = float(self.inputs["v_compra"].get().replace(",", ".") or 0)
            imp = float(self.inputs["imposto"].get().replace(",", ".") or 0)/100
            fix = float(self.inputs["custo_fixo"].get().replace(",", ".") or 0)/100
            mrg = float(self.inputs["margem_lucro"].get().replace(",", ".") or 0)/100
            venda = compra + (compra * (imp + fix + mrg))
            self.inputs["v_venda"].configure(state="normal")
            self.inputs["v_venda"].delete(0, 'end'); self.inputs["v_venda"].insert(0, f"R$ {venda:.2f}")
            self.inputs["v_venda"].configure(state="readonly")
        except: pass

    def iniciar_busca(self):
        termo = self.inputs["produto"].get()
        res = database.buscar_produtos_flexivel(termo)
        if res: 
            from produtos import JanelaBusca
            JanelaBusca(res, self.preencher_campos, "produto")
        else: messagebox.showinfo("Busca", "Não encontrado.")

    def preencher_campos(self, item):
        self.resetar_interface()
        for k, v in item.items():
            if k in self.inputs:
                if isinstance(self.inputs[k], ctk.CTkEntry):
                    self.inputs[k].configure(state="normal")
                    self.inputs[k].delete(0, 'end'); self.inputs[k].insert(0, str(v))
                else: self.inputs[k].set(str(v))
        self.inputs["v_venda"].configure(state="readonly")
        self.id_original = (item['produto'], item['fabricante'])
        self.modo_edicao = True
        
        y_btn = 460
        self.btn_buscar.place_forget()
        self.btn_retornar.place(x=300, y=y_btn)
        self.btn_deletar.place(x=450, y=y_btn)

    def fluxo_salvamento(self):
        dados = {}
        for c, e in self.inputs.items():
            valor = e.get().replace("R$", "").replace(",", ".").strip()
            dados[c] = valor

        if self.modo_edicao:
            if database.atualizar_produto_composto(dados, self.id_original[0], self.id_original[1]):
                messagebox.showinfo("Sucesso", "Atualizado!")
        else:
            if database.salvar_produto(dados): 
                messagebox.showinfo("Sucesso", "Salvo!")
            else: 
                messagebox.showerror("Erro", "Produto/Fabricante já existe!")
        self.resetar_interface()

    def excluir_produto(self):
        if messagebox.askyesno("Confirma", "Excluir item?"):
            database.deletar_produto_composto(self.id_original[0], self.id_original[1])
            self.resetar_interface()

    def resetar_interface(self):
        for e in self.inputs.values():
            if isinstance(e, ctk.CTkEntry): 
                e.configure(state="normal")
                e.delete(0, 'end')
        self.inputs["v_venda"].configure(state="readonly")
        self.id_original = None
        self.modo_edicao = False
        
        y_btn = 460
        self.btn_deletar.place_forget()
        self.btn_retornar.place_forget()
        self.btn_buscar.place(x=300, y=y_btn)
        
class Servicos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}          
        self.desc_original = None 
        self.modo_edicao = False  

    def abrir_servicos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")
        
        # Garante que a coluna 1 (onde estão os campos) se ajuste
        self.grid_columnconfigure(1, weight=1)

        # --- CABEÇALHO PADRONIZADO (LARGURA TOTAL) ---
        header = ctk.CTkFrame(self, fg_color="#145B06", height=50, corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew") # sticky="ew" faz ocupar tudo
        header.grid_propagate(False)
        
        ctk.CTkLabel(header, text="🛠️ CADASTRO DE SERVIÇOS", 
                     font=("Arial", 16, "bold"), text_color="white").pack(pady=12)

        # Espaçador
        ctk.CTkLabel(self, text="", height=10).grid(row=1, column=0)

        campos = [
            ("Descrição:", "descricao", "Manutenção...", self.aplicar_titulo),
            ("Valor Custo:", "v_custo", "0.00", None),
            ("Custo Fixo (%):", "v_fixo", "0", None),
            ("Imposto (%):", "v_imposto", "0", None),
            ("Margem Lucro (%):", "v_margem", "0", None),
            ("Preço Final:", "v_final", "R$ 0,00", None)
        ]
        
        for i, (txt, chave, msg, func) in enumerate(campos):
            ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06").grid(row=i+2, column=0, padx=25, pady=5, sticky="w")
            
            est = "readonly" if chave == "v_final" else "normal"
            entry = ctk.CTkEntry(self, width=400, height=35, placeholder_text=msg, state=est, 
                                 fg_color="#F0F0F0" if est=="normal" else "#E0E0E0", 
                                 border_width=0, corner_radius=50, text_color="black")
            
            if func: entry.bind("<KeyRelease>", lambda event, e=entry, f=func: f(e))
            if chave in ["v_custo", "v_fixo", "v_imposto", "v_margem"]:
                entry.bind("<KeyRelease>", lambda e: self.calcular_servico(), add="+")
                
            entry.grid(row=i+2, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = entry 

        # Botões de ação reposicionados
        y_btn = 400
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", width=120, height=35, fg_color="#2E8B57", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.fluxo_salvamento)
        self.btn_salvar.place(x=150, y=y_btn)
        
        self.btn_buscar = ctk.CTkButton(self, text="BUSCAR", width=120, height=35, fg_color="#D2691E", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.iniciar_busca)
        self.btn_buscar.place(x=300, y=y_btn)
        
        self.btn_retornar = ctk.CTkButton(self, text="RETORNAR", width=120, height=35, fg_color="#696969", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.resetar_interface)
        
        self.btn_deletar = ctk.CTkButton(self, text="DELETAR", width=120, height=35, fg_color="#B22222", hover_color="#145B06", font=("Arial", 12, "bold"), command=self.excluir_servico)

   
    # Formata o texto para "Formato De Título" (primeiras letras maiúsculas)
    def aplicar_titulo(self, e):
        t = e.get().title(); p = e.index("insert"); e.delete(0, "end"); e.insert(0, t); e.icursor(p)

    # Realiza o cálculo do preço final do serviço somando as porcentagens ao custo base
    def calcular_servico(self):
        try:
            # Converte os textos em números decimais (float), trocando vírgula por ponto
            custo = float(self.inputs["v_custo"].get().replace(",", ".") or 0)
            fix = float(self.inputs["v_fixo"].get().replace(",", ".") or 0)/100
            imp = float(self.inputs["v_imposto"].get().replace(",", ".") or 0)/100
            mrg = float(self.inputs["v_margem"].get().replace(",", ".") or 0)/100
            
            # Cálculo: Custo + (Custo * Soma das Taxas)
            total = custo + (custo * (fix + imp + mrg))
            
            # Atualiza o campo "Preço Final" (precisa mudar o estado para 'normal' antes de editar)
            self.inputs["v_final"].configure(state="normal")
            self.inputs["v_final"].delete(0, 'end'); self.inputs["v_final"].insert(0, f"R$ {total:.2f}")
            self.inputs["v_final"].configure(state="readonly")
        except: pass # Ignora erros de digitação durante o cálculo

    # Inicia a pesquisa de serviços no banco de dados
    def iniciar_busca(self):
        termo = self.inputs["descricao"].get()
        res = database.buscar_servicos_flexivel(termo)
        if res: 
            # Abre a janela de seleção com os resultados encontrados
            JanelaBusca(res, self.preencher_campos, "servico")
        else: 
            messagebox.showinfo("Busca", "Não encontrado.")

    # Preenche os campos da tela com os dados do serviço escolhido na busca
        # Preenche os campos da tela com os dados do serviço escolhido na busca
    def preencher_campos(self, item):
        self.resetar_interface()
        for c, v in item.items():
            if c in self.inputs:
                self.inputs[c].configure(state="normal")
                self.inputs[c].delete(0, 'end'); self.inputs[c].insert(0, str(v))
        self.inputs["v_final"].configure(state="readonly")
        self.desc_original = item['descricao'] 
        self.modo_edicao = True                
        
        # --- AJUSTE DE ALINHAMENTO ---
        y_padrao = 400 
        self.btn_buscar.place_forget()         
        self.btn_retornar.place(x=300, y=y_padrao)  
        self.btn_deletar.place(x=450, y=y_padrao)   

    # Limpa todos os campos e restaura os botões originais da tela
    def resetar_interface(self):
        for e in self.inputs.values(): 
            e.configure(state="normal")
            e.delete(0, 'end')
        self.inputs["v_final"].configure(state="readonly")
        self.desc_original = None
        self.modo_edicao = False
        
        # --- AJUSTE DE ALINHAMENTO ---
        y_padrao = 400
        self.btn_deletar.place_forget()
        self.btn_retornar.place_forget()
        self.btn_buscar.place(x=300, y=y_padrao)

    # Gerencia o salvamento dos dados (Insert ou Update)
    def fluxo_salvamento(self):
        # LIMPEZA DOS DADOS
        dados = {c: e.get().replace("R$", "").replace(",", ".").strip() for c, e in self.inputs.items()}
        
        if self.modo_edicao:
            # O nome correto conforme seu database.py é atualizar_servico
            if database.atualizar_servico(dados, self.desc_original):
                messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar no banco.")

        else:
            database.salvar_servico(dados)
            messagebox.showinfo("Sucesso", "Salvo!")
        self.resetar_interface()


    # Remove o serviço do banco de dados após confirmação
    def excluir_servico(self):
        if messagebox.askyesno("Confirma", "Excluir?"):
            database.deletar_servico(self.desc_original); self.resetar_interface()

    # Limpa todos os campos e restaura os botões originais da tela
    def resetar_interface(self):
        for e in self.inputs.values(): 
            e.configure(state="normal")
            e.delete(0, 'end')
        
        self.inputs["v_final"].configure(state="readonly")
        self.desc_original = None
        self.modo_edicao = False
        
        # --- CORREÇÃO DO POSICIONAMENTO ---
        y_padrao = 400 # O mesmo y que você usou no abrir_servicos
        self.btn_deletar.place_forget()
        self.btn_retornar.place_forget()
        
        # Aqui estava 350, por isso ele "pulava" para cima ou sumia
        self.btn_buscar.place(x=300, y=y_padrao) 


