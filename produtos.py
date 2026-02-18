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

# --- CLASSE DE PRODUTOS ---
# Define o painel de gerenciamento de produtos herdando de CTkFrame (um quadro da interface)
class Produtos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Inicializa a classe pai (Frame)
        super().__init__(master, **kwargs)
        self.inputs = {}          # Dicionário para guardar as referências de cada campo de entrada
        self.id_original = None   # Armazena o ID (Nome/Fabricante) para saber qual item editar
        self.modo_edicao = False  # Controla se o botão 'Salvar' deve criar um novo ou atualizar existente

    # Método que desenha a interface na tela
    def abrir_produtos(self):
        # Faz o frame ocupar toda a janela e define o fundo branco
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")
        
        # Lista de configuração dos campos: (Rótulo, Chave, Placeholder, Tipo, Função_ao_digitar)
        campos = [
            ("Produto:", "produto", "Nome...", "entry", self.aplicar_titulo),
            ("Fabricante:", "fabricante", "Fabricante...", "entry", self.aplicar_titulo),
            ("Valor Compra:", "v_compra", "0.00", "entry", None),
            ("Custo Fixo (%):", "custo_fixo", "0", "entry", None),
            ("Imposto (%):", "imposto", "0", "entry", None),
            ("Margem Lucro (%):", "margem_lucro", "0", "entry", None),
            ("Quantidade:", "quantidade", "0", "entry", None),
            ("Unidade:", "unidade", ["UNI", "KG", "CX"], "combo", None),
            ("Venda Final:", "v_venda", "R$ 0,00", "entry", None)
        ]

        # Loop para criar automaticamente cada Label e Input na tela usando Grid
        for i, (txt, chave, msg, tipo, func) in enumerate(campos):
            # Cria o texto à esquerda (Label)
            ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06").grid(row=i, column=0, padx=10, pady=3, sticky="w")
            
            if tipo == "entry":
                # Cria campo de texto simples
                widget = ctk.CTkEntry(self, width=400, height=35, placeholder_text=msg, fg_color="#F0F0F0", border_width=0, corner_radius=50, text_color="black")
                # Se for o campo de venda, bloqueia para digitação (é preenchido por cálculo)
                if chave == "v_venda": widget.configure(state="readonly", fg_color="#E0E0E0")
                # Se houver função de formatação (como Título), aplica ao soltar a tecla
                if func: widget.bind("<KeyRelease>", lambda event, e=widget, f=func: f(e))
                # Se for campo numérico, vincula o cálculo automático de preço
                if chave in ["v_compra", "imposto", "custo_fixo", "margem_lucro"]:
                    widget.bind("<KeyRelease>", lambda e: self.calcular_venda(), add="+")
            else:
                # Cria caixa de seleção (Combo)
                widget = ctk.CTkComboBox(self, width=400, height=35, values=msg, fg_color="#F0F0F0", border_width=0, corner_radius=50, text_color="black")
            
            # Posiciona o widget na coluna 1 da grade
            widget.grid(row=i, column=1, padx=5, pady=3, sticky="w")
            self.inputs[chave] = widget # Salva o widget no dicionário usando a chave técnica

        # Configura os botões de ação com suas respectivas cores e comandos
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", width=120, fg_color="#2E8B57", command=self.fluxo_salvamento)
        self.btn_salvar.place(x=150, y=420)
        self.btn_buscar = ctk.CTkButton(self, text="BUSCAR", width=120, fg_color="#D2691E", command=self.iniciar_busca)
        self.btn_buscar.place(x=300, y=420)
        self.btn_retornar = ctk.CTkButton(self, text="RETORNAR", width=120, fg_color="#696969", command=self.resetar_interface)
        self.btn_deletar = ctk.CTkButton(self, text="DELETAR", width=120, fg_color="#B22222", command=self.excluir_produto)

    # Função que deixa a primeira letra maiúscula enquanto o usuário digita
    def aplicar_titulo(self, e):
        t = e.get().title(); p = e.index("insert"); e.delete(0, "end"); e.insert(0, t); e.icursor(p)

    # Realiza a conta matemática para projetar o valor de venda final
    def calcular_venda(self):
        try:
            # Captura os valores e trata vírgula para ponto decimal
            compra = float(self.inputs["v_compra"].get().replace(",", ".") or 0)
            imp = float(self.inputs["imposto"].get().replace(",", ".") or 0)/100
            fix = float(self.inputs["custo_fixo"].get().replace(",", ".") or 0)/100
            mrg = float(self.inputs["margem_lucro"].get().replace(",", ".") or 0)/100
            # Aplica a soma das porcentagens sobre o valor base
            venda = compra + (compra * (imp + fix + mrg))
            # Atualiza o campo de venda (abre para escrita, limpa, escreve e bloqueia de novo)
            self.inputs["v_venda"].configure(state="normal")
            self.inputs["v_venda"].delete(0, 'end'); self.inputs["v_venda"].insert(0, f"R$ {venda:.2f}")
            self.inputs["v_venda"].configure(state="readonly")
        except: pass # Se o usuário digitar algo que não seja número, ignora o erro

    # Inicia o processo de pesquisa no banco de dados
    def iniciar_busca(self):
        termo = self.inputs["produto"].get()
        res = database.buscar_produtos_flexivel(termo) # Chama a função do seu arquivo database.py
        if res: JanelaBusca(res, self.preencher_campos, "produto") # Abre a pop-up que comentamos antes
        else: messagebox.showinfo("Busca", "Não encontrado.")

    # Pega os dados de um produto selecionado na busca e coloca nas caixas de texto
    def preencher_campos(self, item):
        self.resetar_interface()
        for k, v in item.items():
            if k in self.inputs:
                if isinstance(self.inputs[k], ctk.CTkEntry):
                    self.inputs[k].configure(state="normal")
                    self.inputs[k].delete(0, 'end'); self.inputs[k].insert(0, str(v))
                else: self.inputs[k].set(str(v))
        self.inputs["v_venda"].configure(state="readonly")
        self.id_original = (item['produto'], item['fabricante']) # Salva a identidade para caso de edição
        self.modo_edicao = True # Muda o comportamento do botão Salvar
        self.btn_buscar.place_forget() # Esconde busca
        self.btn_retornar.place(x=300, y=420) # Mostra retorno
        self.btn_deletar.place(x=450, y=420) # Mostra exclusão

    # Gerencia se o sistema deve criar um registro novo ou atualizar um antigo
    def fluxo_salvamento(self):
    # LIMPEZA DOS DADOS: Remove "R$", espaços e garante que use ponto em vez de vírgula
        dados = {}
        for c, e in self.inputs.items():
            valor = e.get().replace("R$", "").replace(",", ".").strip()
            dados[c] = valor

        if self.modo_edicao:
            database.atualizar_produto_composto(dados, self.id_original[0], self.id_original[1])
            messagebox.showinfo("Sucesso", "Atualizado!")
        else:
            if database.salvar_produto(dados): 
                messagebox.showinfo("Sucesso", "Salvo!")
            else: 
                messagebox.showerror("Erro", "Produto/Fabricante já existe!")
        self.resetar_interface()


    # Pergunta se o usuário tem certeza e deleta o item
    def excluir_produto(self):
        if messagebox.askyesno("Confirma", "Excluir item?"):
            database.deletar_produto_composto(self.id_original[0], self.id_original[1]); self.resetar_interface()

    # Limpa todos os campos e volta os botões ao estado original (Novo Cadastro)
    def resetar_interface(self):
        for e in self.inputs.values():
            if isinstance(e, ctk.CTkEntry): e.configure(state="normal"); e.delete(0, 'end')
        self.inputs["v_venda"].configure(state="readonly")
        self.id_original = None; self.modo_edicao = False
        self.btn_deletar.place_forget(); self.btn_retornar.place_forget()
        self.btn_buscar.place(x=300, y=420)
# --- CLASSE DE SERVIÇOS ---
# Define o painel de gerenciamento de serviços (ex: mão de obra, manutenção)
class Servicos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}          # Dicionário para armazenar as referências dos campos de entrada
        self.desc_original = None # Armazena a descrição original para identificar o item na edição
        self.modo_edicao = False  # Flag que indica se estamos editando ou criando um novo serviço

    # Método para construir a interface visual de serviços
    def abrir_servicos(self):
        # Posiciona o frame preenchendo toda a tela e define cor branca
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")
        
        # Lista de campos: (Rótulo, Chave técnica, Texto de exemplo, Função de formatação)
        campos = [
            ("Descrição:", "descricao", "Manutenção...", self.aplicar_titulo),
            ("Valor Custo:", "v_custo", "0.00", None),
            ("Custo Fixo (%):", "v_fixo", "0", None),
            ("Imposto (%):", "v_imposto", "0", None),
            ("Margem Lucro (%):", "v_margem", "0", None),
            ("Preço Final:", "v_final", "R$ 0,00", None)
        ]
        
        # Loop para criar os campos (Labels e Entries) dinamicamente
        for i, (txt, chave, msg, func) in enumerate(campos):
            # Cria o rótulo (Label) verde à esquerda
            ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            # Define se o campo será apenas leitura (para o Preço Final) ou normal
            est = "readonly" if chave == "v_final" else "normal"
            
            # Cria a caixa de entrada (Entry) com bordas arredondadas (corner_radius=50)
            entry = ctk.CTkEntry(self, width=400, height=35, placeholder_text=msg, state=est, 
                                 fg_color="#F0F0F0" if est=="normal" else "#E0E0E0", 
                                 border_width=0, corner_radius=50, text_color="black")
            
            # Se houver função (como aplicar_titulo), vincula ao evento de soltar a tecla
            if func: entry.bind("<KeyRelease>", lambda event, e=entry, f=func: f(e))
            
            # Se for um campo de valor, vincula ao cálculo automático do preço final
            if chave in ["v_custo", "v_fixo", "v_imposto", "v_margem"]:
                entry.bind("<KeyRelease>", lambda e: self.calcular_servico(), add="+")
                
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = entry # Guarda a referência no dicionário

        # Configuração e posicionamento dos botões de ação
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", width=120, fg_color="#2E8B57", command=self.fluxo_salvamento)
        self.btn_salvar.place(x=150, y=350)
        self.btn_buscar = ctk.CTkButton(self, text="BUSCAR", width=120, fg_color="#D2691E", command=self.iniciar_busca)
        self.btn_buscar.place(x=300, y=350)
        self.btn_retornar = ctk.CTkButton(self, text="RETORNAR", width=120, fg_color="#696969", command=self.resetar_interface)
        self.btn_deletar = ctk.CTkButton(self, text="DELETAR", width=120, fg_color="#B22222", command=self.excluir_servico)

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
    def preencher_campos(self, item):
        self.resetar_interface()
        for c, v in item.items():
            if c in self.inputs:
                self.inputs[c].configure(state="normal")
                self.inputs[c].delete(0, 'end'); self.inputs[c].insert(0, str(v))
        self.inputs["v_final"].configure(state="readonly")
        self.desc_original = item['descricao'] # Salva a descrição para referência na atualização
        self.modo_edicao = True                # Ativa o modo de edição
        self.btn_buscar.place_forget()         # Oculta botão de busca
        self.btn_retornar.place(x=300, y=350)  # Mostra botão de retornar
        self.btn_deletar.place(x=450, y=350)   # Mostra botão de exclusão

    # Gerencia o salvamento dos dados (Insert ou Update)
    def fluxo_salvamento(self):
        # LIMPEZA DOS DADOS
        dados = {c: e.get().replace("R$", "").replace(",", ".").strip() for c, e in self.inputs.items()}
        
        if self.modo_edicao:
            database.atualizar_servico_com_desc(dados, self.desc_original)
            messagebox.showinfo("Sucesso", "Atualizado!")
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
        for e in self.inputs.values(): e.configure(state="normal"); e.delete(0, 'end')
        self.inputs["v_final"].configure(state="readonly")
        self.desc_original = None; self.modo_edicao = False
        self.btn_deletar.place_forget(); self.btn_retornar.place_forget()
        self.btn_buscar.place(x=300, y=350)

