import customtkinter as ctk
import database # Importa a lógica de persistência para salvar produtos e serviços

# --- CLASSE PARA CADASTRO DE PRODUTOS ---
class Produtos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {} # Dicionário para mapear os widgets de entrada

    def abrir_produtos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        # Lista de configuração: centraliza rótulos, chaves, placeholders e o TIPO do widget
        campos = [
            ("Produto:", "produto", "Nome do item...", "entry"),
            ("Marca:", "marca", "Fabricante ou marca...", "entry"),
            ("Valor Compra:", "v_compra", "R$ 0,00", "entry"),
            ("Imposto (%):", "imposto", "0", "entry"),
            ("Custo Fixo (%):", "custo_fixo", "0", "entry"),
            ("Margem Lucro (%):", "margem_lucro", "0", "entry"),
            ("Quantidade:", "quantidade", "Ex: 10", "entry"),
            ("Unidade:", "unidade", ["UNI", "Metro", "Rolo", "KG", "CX"], "combo"), # Widget seletor
            ("Venda Final:", "v_venda", "Cálculo automático...", "entry")
        ]

        for i, (txt, chave, msg, tipo) in enumerate(campos):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")

            if tipo == "entry":
                # Lógica para o campo 'Venda Final': ele deve ser apenas leitura (readonly)
                estado = "readonly" if chave == "v_venda" else "normal"
                cor_fundo = "#E0E0E0" if chave == "v_venda" else "#F0F0F0"
                
                widget = ctk.CTkEntry(
                    self, width=400, height=40, font=("Arial", 16, "bold"),
                    placeholder_text=msg, fg_color=cor_fundo, bg_color="white",
                    border_width=0, corner_radius=50, text_color="black", state=estado
                )
                
                # BIND (Vínculo): Chama a função de cálculo toda vez que uma tecla é solta
                if chave in ["v_compra", "imposto", "custo_fixo", "margem_lucro"]:
                    widget.bind("<KeyRelease>", lambda event: self.calcular_venda())
            else:
                # CTkComboBox: Cria uma lista de seleção para evitar erros de digitação na unidade
                widget = ctk.CTkComboBox(
                    self, width=400, height=40, font=("Arial", 16, "bold"),
                    values=msg, fg_color="#F0F0F0", bg_color="white",
                    border_width=0, corner_radius=50, text_color="black",
                    button_color="#2E8B57", button_hover_color="#145B06"
                )

            widget.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = widget

        # Botão Salvar associado ao método de gravação no banco
        self.btn_salvar = ctk.CTkButton(
            self, text="SALVAR", fg_color="#2E8B57", hover_color="#145B06",
            font=("Arial", 14, "bold"), corner_radius=50, command=self.salvar_produtos
        )
        self.btn_salvar.grid(row=len(campos), column=1, pady=20, sticky="e", padx=5)

    def calcular_venda(self):
        """Realiza o cálculo automático do preço de venda com base nos percentuais."""
        try:
            # Tratamento de erro: se o campo estiver vazio, considera 0 para não quebrar o cálculo
            compra = float(self.inputs["v_compra"].get().replace(",", ".") or 0)
            imposto_p = float(self.inputs["imposto"].get().replace(",", ".") or 0) / 100
            fixo_p = float(self.inputs["custo_fixo"].get().replace(",", ".") or 0) / 100
            margem_p = float(self.inputs["margem_lucro"].get().replace(",", ".") or 0) / 100
            
            # Fórmula: Soma dos percentuais aplicados sobre o valor base
            venda_final = compra + (compra * imposto_p) + (compra * fixo_p) + (compra * margem_p)

            # Atualização do widget: Temporariamente 'normal' para inserir texto, depois volta a ser travado
            self.inputs["v_venda"].configure(state="normal")
            self.inputs["v_venda"].delete(0, 'end')
            self.inputs["v_venda"].insert(0, f"R$ {venda_final:.2f}")
            self.inputs["v_venda"].configure(state="readonly")
        except ValueError:
            # Captura erros caso o usuário digite letras onde deveriam ser números
            pass

    def salvar_produtos(self):
        """Coleta os dados e aciona o banco de dados."""
        dados = {chave: input_field.get() for chave, input_field in self.inputs.items()}
        database.salvar_produto(dados) # Gravação via SQL no SQLite
        
        # Reset da interface após o salvamento
        for chave, input_field in self.inputs.items():
            if isinstance(input_field, ctk.CTkEntry):
                input_field.configure(state="normal")
                input_field.delete(0, 'end')
                if chave == "v_venda":
                    input_field.configure(state="readonly")
            elif isinstance(input_field, ctk.CTkComboBox):
                input_field.set("UNI")
        self.inputs["produto"].focus()


# --- CLASSE PARA CADASTRO DE SERVIÇOS ---
class Servicos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}

    def abrir_servicos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.configure(fg_color="white")

        campos_serv = [
            ("Descrição:", "descricao", "Ex: Manutenção..."),
            ("Valor Custo:", "v_custo", "Custos operacionais..."),
            ("Custo Fixo (%):", "v_fixo", "Percentual fixo..."),
            ("Valor Imposto (%):", "v_imposto", "Impostos..."),
            ("Margem Lucro (%):", "v_margem", "Percentual de lucro..."),
            ("Preço do Serviço:", "v_final", "Cálculo automático...")
        ]

        # Construção da grade de serviços (similar aos produtos)
        for i, (txt, chave, msg) in enumerate(campos_serv):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")

            estado = "readonly" if chave == "v_final" else "normal"
            cor_fundo = "#E0E0E0" if chave == "v_final" else "#F0F0F0"

            entry = ctk.CTkEntry(
                self, width=400, height=40, font=("Arial", 16, "bold"),
                placeholder_text=msg, fg_color=cor_fundo, bg_color="white",
                border_width=0, corner_radius=50, text_color="black", state=estado
            )
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[chave] = entry

            # Vínculo para cálculo dinâmico do serviço
            if chave in ["v_custo", "v_fixo", "v_imposto", "v_margem"]:
                entry.bind("<KeyRelease>", lambda event: self.calcular_servico())

        self.btn_salvar = ctk.CTkButton(
            self, text="SALVAR", fg_color="#2E8B57", hover_color="#145B06",
            font=("Arial", 14, "bold"), corner_radius=50, command=self.salvar_servicos
        )
        self.btn_salvar.grid(row=len(campos_serv), column=1, pady=20, sticky="e", padx=5)

    def calcular_servico(self):
        """Aplica margens e custos sobre o valor base do serviço."""
        try:
            custo = float(self.inputs["v_custo"].get().replace(",", ".") or 0)
            fixo_p = float(self.inputs["v_fixo"].get().replace(",", ".") or 0) / 100
            imposto_p = float(self.inputs["v_imposto"].get().replace(",", ".") or 0) / 100
            margem_p = float(self.inputs["v_margem"].get().replace(",", ".") or 0) / 100
            preco_final = custo + (custo * fixo_p) + (custo * imposto_p) + (custo * margem_p)

            self.inputs["v_final"].configure(state="normal")
            self.inputs["v_final"].delete(0, 'end')
            self.inputs["v_final"].insert(0, f"R$ {preco_final:.2f}")
            self.inputs["v_final"].configure(state="readonly")
        except ValueError:
            pass

    def salvar_servicos(self):
        """Salva o serviço no banco e reseta a tela."""
        dados = {chave: input_field.get() for chave, input_field in self.inputs.items()}
        database.salvar_servico(dados)
        
        for input_field in self.inputs.values():
            input_field.configure(state="normal")
            input_field.delete(0, 'end')
        self.inputs["v_final"].configure(state="readonly")
        self.inputs["descricao"].focus()
