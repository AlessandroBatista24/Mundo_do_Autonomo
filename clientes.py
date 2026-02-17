import customtkinter as ctk 
import database 
from tkinter import messagebox
import re

class PessoaFisica(ctk.CTkFrame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) 
        self.inputs = {} 
        self.editando_cpf = None 

    def abrir_fisica(self):
        self.place(x=0, y=0, relwidth=1, relheight=1) 
        self.configure(fg_color="white") 

        campos_pf = [
            ("Nome do Cliente:", "nome", "Digite o nome completo...", self.aplicar_titulo),
            ("CPF:", "cpf", "000.000.000-00", self.mascara_cpf), 
            ("Endereço:", "logradouro", "Rua, Avenida...", self.aplicar_titulo),
            ("Número:", "numero", "Nº", None),
            ("Bairro:", "bairro", "Bairro...", self.aplicar_titulo),
            ("Cidade:", "cidade", "Cidade...", self.aplicar_titulo),
            ("Estado:", "estado", "UF", self.aplicar_titulo),
            ("CEP:", "cep", "00.000-000", self.mascara_cep),
            ("Telefone:", "telefone", "(00) 00000-0000", self.mascara_telefone),
            ("Email:", "email", "exemplo@email.com", None)
        ]

        for i, (txt, chave, msg, func) in enumerate(campos_pf):
            ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06").grid(row=i, column=0, padx=10, pady=3, sticky="w")
            entry = ctk.CTkEntry(self, width=400, height=35, placeholder_text=msg, fg_color="#F0F0F0", border_width=0, corner_radius=50, text_color="black")
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="w") 
            if func: entry.bind("<KeyRelease>", lambda event, e=entry, f=func: f(e))
            self.inputs[chave] = entry 

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=len(campos_pf), column=1, pady=20, sticky="w")

        self.btn_salvar = ctk.CTkButton(self.frame_botoes, text="SALVAR", width=120, fg_color="#2E8B57", command=self.fluxo_salvamento)
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_aux = ctk.CTkButton(self.frame_botoes, text="Editar", width=120, fg_color="#145B06", command=self.alternar_modo)
        self.btn_aux.pack(side="left", padx=5)

        self.btn_deletar = ctk.CTkButton(self.frame_botoes, text="DELETAR", width=120, fg_color="#E20B0B", command=self.excluir_pf)

    def aplicar_titulo(self, e): 
        texto = e.get().title()
        pos = e.index("insert")
        e.delete(0, "end"); e.insert(0, texto); e.icursor(pos)

    def mascara_cpf(self, e):
        v = "".join(filter(str.isdigit, e.get()))
        if len(v) <= 3: fmt = v
        elif len(v) <= 6: fmt = f"{v[:3]}.{v[3:]}"
        elif len(v) <= 9: fmt = f"{v[:3]}.{v[3:6]}.{v[6:]}"
        else: fmt = f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:11]}"
        e.delete(0, "end"); e.insert(0, fmt[:14])

    def mascara_cep(self, e):
        v = "".join(filter(str.isdigit, e.get()))
        fmt = f"{v[:2]}.{v[2:5]}-{v[5:8]}" if len(v) > 5 else v
        e.delete(0, "end"); e.insert(0, fmt[:10])

    def mascara_telefone(self, e):
        v = "".join(filter(str.isdigit, e.get()))
        fmt = f"({v[:2]}) {v[2:7]}-{v[7:11]}" if len(v) > 7 else v
        e.delete(0, "end"); e.insert(0, fmt[:15])

    def validar_email(self, email):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

    def alternar_modo(self):
        if self.btn_aux.cget("text") == "Editar":
            self.limpar_campos(); self.btn_salvar.configure(text="BUSCAR CPF", fg_color="#D2691E")
            self.btn_aux.configure(text="Retornar", fg_color="#555555"); self.inputs["cpf"].focus()
        else: self.resetar_interface()

    def fluxo_salvamento(self):
        t = self.btn_salvar.cget("text")
        if t == "BUSCAR CPF":
            if not self.inputs["cpf"].get().strip(): return messagebox.showwarning("Erro", "Digite o CPF!")
            self.buscar_pf(); return
        for k, v in self.inputs.items():
            if not v.get().strip(): return messagebox.showwarning("Erro", f"Campo {k.upper()} vazio!")
        if not self.validar_email(self.inputs["email"].get().strip()): return messagebox.showerror("Erro", "E-mail inválido!")
        if t == "SALVAR ALTERAÇÕES": self.finalizar_edicao()
        else: self.salvar_novo()

    def buscar_pf(self):
        c = database.buscar_cliente_pf_por_cpf(self.inputs["cpf"].get())
        if c:
            for k, v in c.items():
                if k in self.inputs: self.inputs[k].delete(0, 'end'); self.inputs[k].insert(0, str(v) if v else "")
            self.editando_cpf = self.inputs["cpf"].get(); self.btn_salvar.configure(text="SALVAR ALTERAÇÕES", fg_color="#2E8B57"); self.btn_deletar.pack(side="left", padx=5)
        else: messagebox.showerror("Erro", "Não encontrado!")

    def finalizar_edicao(self):
        database.atualizar_cliente_pf({k: v.get() for k, v in self.inputs.items()}); self.resetar_interface()

    def salvar_novo(self):
        database.salvar_cliente_pf({k: v.get() for k, v in self.inputs.items()}); self.limpar_campos()

    def excluir_pf(self):
        if messagebox.askyesno("Confirma", "Deletar?"): database.deletar_cliente_pf(self.editando_cpf); self.resetar_interface()

    def limpar_campos(self):
        for e in self.inputs.values(): e.delete(0, 'end')

    def resetar_interface(self):
        self.limpar_campos(); self.editando_cpf = None; self.btn_salvar.configure(text="SALVAR", fg_color="#2E8B57")
        self.btn_aux.configure(text="Editar", fg_color="#145B06"); self.btn_deletar.pack_forget()

class PessoaJuridica(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}
        self.editando_cnpj = None

    def abrir_juridico(self):
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")
        campos_pj = [
            ("Razão Social:", "empresa", "Empresa...", self.aplicar_titulo),
            ("Nome Fantasia:", "fantasia", "Nome fantasia...", self.aplicar_titulo),
            ("CNPJ:", "cnpj", "00.000.000/0000-00", self.mascara_cnpj),
            ("Inscrição:", "inscricao", "Estadual/Municipal...", None),
            ("Endereço:", "logradouro", "Rua...", self.aplicar_titulo),
            ("Número:", "numero", "Nº", None),
            ("Bairro:", "bairro", "Bairro...", self.aplicar_titulo),
            ("Cidade:", "cidade", "Cidade...", self.aplicar_titulo),
            ("Estado:", "estado", "UF", self.aplicar_titulo),
            ("CEP:", "cep", "00.000-000", self.mascara_cep),
            ("Telefone:", "telefone", "(00) 0000-0000", self.mascara_telefone),
            ("Email:", "email", "email@empresa.com", None)
        ]
        for i, (txt, chave, msg, func) in enumerate(campos_pj):
            ctk.CTkLabel(self, text=txt, font=("Arial", 14, "bold"), text_color="#145B06").grid(row=i, column=0, padx=10, pady=3, sticky="w")
            entry = ctk.CTkEntry(self, width=400, height=35, placeholder_text=msg, fg_color="#F0F0F0", border_width=0, corner_radius=50, text_color="black")
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="w") 
            if func: entry.bind("<KeyRelease>", lambda event, e=entry, f=func: f(e))
            self.inputs[chave] = entry 

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=len(campos_pj), column=1, pady=20, sticky="w")
        self.btn_salvar = ctk.CTkButton(self.frame_botoes, text="SALVAR", width=120, fg_color="#2E8B57", command=self.fluxo_salvamento)
        self.btn_salvar.pack(side="left", padx=5)
        self.btn_aux = ctk.CTkButton(self.frame_botoes, text="Editar", width=120, fg_color="#145B06", command=self.alternar_modo)
        self.btn_aux.pack(side="left", padx=5)
        self.btn_deletar = ctk.CTkButton(self.frame_botoes, text="DELETAR", width=120, fg_color="#E20B0B", command=self.excluir_pj)

    def aplicar_titulo(self, e): PessoaFisica.aplicar_titulo(self, e)
    def mascara_cep(self, e): PessoaFisica.mascara_cep(self, e)
    def mascara_telefone(self, e): PessoaFisica.mascara_telefone(self, e)
    def validar_email(self, e): return PessoaFisica.validar_email(self, e)
    
    def mascara_cnpj(self, entry):
        v = "".join(filter(str.isdigit, entry.get()))
        if len(v) <= 2: fmt = v
        elif len(v) <= 5: fmt = f"{v[:2]}.{v[2:]}"
        elif len(v) <= 8: fmt = f"{v[:2]}.{v[2:5]}.{v[5:]}"
        elif len(v) <= 12: fmt = f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:]}"
        else: fmt = f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:14]}"
        entry.delete(0, "end"); entry.insert(0, fmt[:18])

    def alternar_modo(self):
        if self.btn_aux.cget("text") == "Editar":
            self.limpar_campos(); self.btn_salvar.configure(text="BUSCAR CNPJ", fg_color="#D2691E")
            self.btn_aux.configure(text="Retornar", fg_color="#555555"); self.inputs["cnpj"].focus()
        else: self.resetar_interface()

    def fluxo_salvamento(self):
        t = self.btn_salvar.cget("text")
        if t == "BUSCAR CNPJ":
            if not self.inputs["cnpj"].get().strip(): return messagebox.showwarning("Erro", "CNPJ vazio!")
            self.buscar_pj(); return
        for k, v in self.inputs.items():
            if not v.get().strip(): return messagebox.showwarning("Erro", f"Campo {k.upper()} vazio!")
        if not self.validar_email(self.inputs["email"].get().strip()): return messagebox.showerror("Erro", "E-mail inválido!")
        if t == "SALVAR ALTERAÇÕES": self.finalizar_edicao_pj()
        else: self.salvar_novo_pj()

    def buscar_pj(self):
        c = database.buscar_cliente_pj_por_cnpj(self.inputs["cnpj"].get())
        if c:
            for k, v in c.items():
                if k in self.inputs: self.inputs[k].delete(0, 'end'); self.inputs[k].insert(0, str(v) if v else "")
            self.editando_cnpj = self.inputs["cnpj"].get(); self.btn_salvar.configure(text="SALVAR ALTERAÇÕES", fg_color="#2E8B57"); self.btn_deletar.pack(side="left", padx=5)
        else: messagebox.showerror("Erro", "Não encontrado!")

    def finalizar_edicao_pj(self): database.atualizar_cliente_pj({k: v.get() for k, v in self.inputs.items()}); self.resetar_interface()
    def salvar_novo_pj(self): database.salvar_cliente_pj({k: v.get() for k, v in self.inputs.items()}); self.limpar_campos()
    def excluir_pj(self):
        if messagebox.askyesno("Confirma", "Deletar?"): database.deletar_cliente_pj(self.editando_cnpj); self.resetar_interface()
    def limpar_campos(self):
        for e in self.inputs.values(): e.delete(0, 'end')
    def resetar_interface(self):
        self.limpar_campos(); self.editando_cnpj = None; self.btn_salvar.configure(text="SALVAR", fg_color="#2E8B57")
        self.btn_aux.configure(text="Editar", fg_color="#145B06"); self.btn_deletar.pack_forget()
