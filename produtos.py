import customtkinter as ctk
import database
from tkinter import messagebox

# --- CLASSE PARA CADASTRO DE PRODUTOS ---
class Produtos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}
        self.editando_produto = None # Armazena o nome original durante a edição

    def abrir_produtos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")

        campos = [
            ("Produto:", "produto", "Nome do item...", "entry", self.aplicar_titulo),
            ("Marca:", "marca", "Fabricante...", "entry", self.aplicar_titulo),
            ("Valor Compra:", "v_compra", "0.00", "entry", None),
            ("Imposto (%):", "imposto", "0", "entry", None),
            ("Custo Fixo (%):", "custo_fixo", "0", "entry", None),
            ("Margem Lucro (%):", "margem_lucro", "0", "entry", None),
            ("Quantidade:", "quantidade", "Ex: 10", "entry", None),
            ("Unidade:", "unidade", ["UNI", "Metro", "Rolo", "KG", "CX"], "combo", None),
            ("Venda Final:", "v_venda", "R$ 0,00", "entry", None)
        ]

        for i, (txt, chave, msg, tipo, mascara) in enumerate(campos):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=3, sticky="w")

            if tipo == "entry":
                estado = "readonly" if chave == "v_venda" else "normal"
                cor_fundo = "#E0E0E0" if chave == "v_venda" else "#F0F0F0"
                widget = ctk.CTkEntry(self, width=400, height=35, font=("Arial", 14), placeholder_text=msg, fg_color=cor_fundo, border_width=0, corner_radius=50, text_color="black", state=estado)
                
                if mascara: widget.bind("<KeyRelease>", lambda event, e=widget, f=mascara: f(e))
                if chave in ["v_compra", "imposto", "custo_fixo", "margem_lucro"]:
                    widget.bind("<KeyRelease>", lambda event: self.calcular_venda(), add="+")
            else:
                widget = ctk.CTkComboBox(self, width=400, height=35, values=msg, fg_color="#F0F0F0", border_width=0, corner_radius=50, text_color="black", button_color="#2E8B57")

            widget.grid(row=i, column=1, padx=5, pady=3, sticky="w")
            self.inputs[chave] = widget

        # Container de Botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=len(campos), column=1, pady=20, sticky="w")

        self.btn_salvar = ctk.CTkButton(self.frame_botoes, text="SALVAR", width=120, fg_color="#2E8B57", command=self.fluxo_salvamento)
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_modo_edicao = ctk.CTkButton(self.frame_botoes, text="MODO EDIÇÃO", width=120, fg_color="#145B06", command=self.ativar_modo_edicao)
        self.btn_modo_edicao.pack(side="left", padx=5)

        self.btn_deletar = ctk.CTkButton(self.frame_botoes, text="DELETAR", width=120, fg_color="#B22222", command=self.excluir_produto)
        self.btn_deletar.pack_forget()

    def aplicar_titulo(self, entry):
        texto = entry.get().title()
        pos = entry.index("insert"); entry.delete(0, "end"); entry.insert(0, texto); entry.icursor(pos)

    def calcular_venda(self):
        try:
            compra = float(self.inputs["v_compra"].get().replace(",", ".") or 0)
            imposto = float(self.inputs["imposto"].get().replace(",", ".") or 0) / 100
            fixo = float(self.inputs["custo_fixo"].get().replace(",", ".") or 0) / 100
            margem = float(self.inputs["margem_lucro"].get().replace(",", ".") or 0) / 100
            venda = compra + (compra * (imposto + fixo + margem))
            self.inputs["v_venda"].configure(state="normal"); self.inputs["v_venda"].delete(0, 'end')
            self.inputs["v_venda"].insert(0, f"R$ {venda:.2f}"); self.inputs["v_venda"].configure(state="readonly")
        except: pass

    def ativar_modo_edicao(self):
        self.resetar_interface()
        self.btn_salvar.configure(text="BUSCAR PRODUTO", fg_color="#D2691E")
        messagebox.showinfo("Edição", "Digite o nome exato do Produto e clique em BUSCAR.")

    def fluxo_salvamento(self):
        texto = self.btn_salvar.cget("text")
        if texto == "BUSCAR PRODUTO":
            nome = self.inputs["produto"].get()
            item = database.buscar_produto_por_nome(nome)
            if item:
                for c, v in item.items():
                    if c in self.inputs:
                        if isinstance(self.inputs[c], ctk.CTkEntry):
                            self.inputs[c].configure(state="normal"); self.inputs[c].delete(0, 'end'); self.inputs[c].insert(0, str(v))
                        else: self.inputs[c].set(str(v))
                self.editando_produto = nome; self.inputs["produto"].configure(state="disabled")
                self.btn_salvar.configure(text="CONFIRMAR ALTERAÇÃO"); self.btn_deletar.pack(side="left", padx=5)
            else: messagebox.showerror("Erro", "Produto não encontrado!")
        
        elif texto == "CONFIRMAR ALTERAÇÃO":
            self.inputs["produto"].configure(state="normal")
            database.atualizar_produto({c: e.get() for c, e in self.inputs.items()})
            messagebox.showinfo("Sucesso", "Produto atualizado!"); self.resetar_interface()
        else:
            if not self.inputs["produto"].get(): return messagebox.showwarning("Aviso", "Nome do produto obrigatório!")
            database.salvar_produto({c: e.get() for c, e in self.inputs.items()})
            messagebox.showinfo("Sucesso", "Salvo!"); self.resetar_interface()

    def excluir_produto(self):
        if messagebox.askyesno("Confirmar", "Excluir este produto?"):
            database.deletar_produto(self.editando_produto); self.resetar_interface()

    def resetar_interface(self):
        self.editando_produto = None
        for e in self.inputs.values():
            if isinstance(e, ctk.CTkEntry): e.configure(state="normal"); e.delete(0, 'end')
            else: e.set("UNI")
        self.inputs["v_venda"].configure(state="readonly")
        self.btn_salvar.configure(text="SALVAR", fg_color="#2E8B57"); self.btn_deletar.pack_forget()

# --- CLASSE PARA CADASTRO DE SERVIÇOS ---
class Servicos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}
        self.editando_servico = None

    def abrir_servicos(self):
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")

        campos = [
            ("Descrição:", "descricao", "Ex: Manutenção...", self.aplicar_titulo),
            ("Valor Custo:", "v_custo", "0.00", None),
            ("Custo Fixo (%):", "v_fixo", "0", None),
            ("Valor Imposto (%):", "v_imposto", "0", None),
            ("Margem Lucro (%):", "v_margem", "0", None),
            ("Preço Final:", "v_final", "R$ 0,00", None)
        ]

        for i, (txt, chave, msg, mascara) in enumerate(campos):
            label = ctk.CTkLabel(self, text=txt, font=("Arial", 16, "bold"), text_color="#145B06")
            label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")
            estado = "readonly" if chave == "v_final" else "normal"
            entry = ctk.CTkEntry(self, width=400, height=40, font=("Arial", 16), placeholder_text=msg, fg_color="#F0F0F0" if estado=="normal" else "#E0E0E0", border_width=0, corner_radius=50, text_color="black", state=estado)
            if mascara: entry.bind("<KeyRelease>", lambda event, e=entry, f=mascara: f(e))
            if chave in ["v_custo", "v_fixo", "v_imposto", "v_margem"]: entry.bind("<KeyRelease>", lambda event: self.calcular_servico(), add="+")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w"); self.inputs[chave] = entry

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=len(campos), column=1, pady=20, sticky="w")
        self.btn_salvar = ctk.CTkButton(self.frame_botoes, text="SALVAR", width=120, fg_color="#2E8B57", command=self.fluxo_servico)
        self.btn_salvar.pack(side="left", padx=5)
        self.btn_modo_edicao = ctk.CTkButton(self.frame_botoes, text="MODO EDIÇÃO", width=120, fg_color="#145B06", command=self.ativar_edicao_serv)
        self.btn_modo_edicao.pack(side="left", padx=5)
        self.btn_deletar = ctk.CTkButton(self.frame_botoes, text="DELETAR", width=120, fg_color="#B22222", command=self.excluir_servico)
        self.btn_deletar.pack_forget()

    def aplicar_titulo(self, entry):
        texto = entry.get().title()
        pos = entry.index("insert"); entry.delete(0, "end"); entry.insert(0, texto); entry.icursor(pos)

    def calcular_servico(self):
        try:
            custo = float(self.inputs["v_custo"].get().replace(",", ".") or 0)
            fixo = float(self.inputs["v_fixo"].get().replace(",", ".") or 0) / 100
            imposto = float(self.inputs["v_imposto"].get().replace(",", ".") or 0) / 100
            margem = float(self.inputs["v_margem"].get().replace(",", ".") or 0) / 100
            v_final = custo + (custo * (fixo + imposto + margem))
            self.inputs["v_final"].configure(state="normal"); self.inputs["v_final"].delete(0, 'end'); self.inputs["v_final"].insert(0, f"R$ {v_final:.2f}"); self.inputs["v_final"].configure(state="readonly")
        except: pass

    def ativar_edicao_serv(self):
        self.resetar_interface(); self.btn_salvar.configure(text="BUSCAR SERVIÇO", fg_color="#D2691E")

    def fluxo_servico(self):
        texto = self.btn_salvar.cget("text")
        if texto == "BUSCAR SERVIÇO":
            desc = self.inputs["descricao"].get()
            item = database.buscar_servico_por_descricao(desc)
            if item:
                for c, v in item.items():
                    if c in self.inputs: self.inputs[c].configure(state="normal"); self.inputs[c].delete(0, 'end'); self.inputs[c].insert(0, str(v))
                self.editando_servico = desc; self.inputs["descricao"].configure(state="disabled"); self.btn_salvar.configure(text="CONFIRMAR ALTERAÇÃO"); self.btn_deletar.pack(side="left", padx=5)
            else: messagebox.showerror("Erro", "Serviço não encontrado!")
        elif texto == "CONFIRMAR ALTERAÇÃO":
            self.inputs["descricao"].configure(state="normal")
            database.atualizar_servico({c: e.get() for c, e in self.inputs.items()})
            messagebox.showinfo("Sucesso", "Serviço atualizado!"); self.resetar_interface()
        else:
            database.salvar_servico({c: e.get() for c, e in self.inputs.items()})
            messagebox.showinfo("Sucesso", "Serviço salvo!"); self.resetar_interface()

    def excluir_servico(self):
        if messagebox.askyesno("Confirmar", "Deletar este serviço?"):
            database.deletar_servico(self.editando_servico); self.resetar_interface()

    def resetar_interface(self):
        self.editando_servico = None
        for e in self.inputs.values(): e.configure(state="normal"); e.delete(0, 'end')
        self.inputs["v_final"].configure(state="readonly")
        self.btn_salvar.configure(text="SALVAR", fg_color="#2E8B57"); self.btn_deletar.pack_forget()
