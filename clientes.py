import customtkinter as ctk     # Biblioteca da interface visual moderna
import database                # Conexão com as funções de Banco de Dados SQL
from tkinter import messagebox  # Para janelas de aviso (Sucesso/Erro)

# =============================================================================
# JANELA AUXILIAR: BUSCA DE CLIENTES (USADA POR PF E PJ)
# =============================================================================
class JanelaBuscaClientes(ctk.CTkToplevel):
    """ Janela flutuante que abre ao clicar em BUSCAR para selecionar um cliente. """
    def __init__(self, resultados, callback, tipo="pf"):
        super().__init__()
        self.title("🔍 Selecionar Cliente")
        self.geometry("550x450")
        self.configure(fg_color="white")     # Fundo branco padrão do software
        self.attributes("-topmost", True)    # Mantém a janela sempre na frente
        self.grab_set()                      # Trava a janela principal até fechar esta
        self.callback = callback             # Função que preencherá os campos na tela principal

        # Cabeçalho Verde Escuro (Identidade Visual)
        header = ctk.CTkFrame(self, fg_color="#145B06", height=50, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="CLIENTES ENCONTRADOS", font=("Arial", 16, "bold"), text_color="white").pack(pady=12)

        # Área de rolagem para listar os resultados encontrados no banco
        self.scroll = ctk.CTkScrollableFrame(self, width=500, height=320, fg_color="white", 
                                            scrollbar_button_color="#2E8B57")
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        for cli in resultados:
            # Define se mostra Nome/CPF ou Empresa/CNPJ conforme o tipo de busca
            nome = cli['nome'] if tipo == "pf" else cli['empresa']
            doc = f"CPF: {cli['cpf']}" if tipo == "pf" else f"CNPJ: {cli['cnpj']}"
            icone = "👤" if tipo == "pf" else "🏢"

            # Card (caixinha) para cada cliente na lista
            card = ctk.CTkFrame(self.scroll, fg_color="#F9F9F9", border_width=1, border_color="#E0E0E0")
            card.pack(fill="x", pady=3, padx=5)

            ctk.CTkLabel(card, text=f"{icone} {nome}", font=("Arial", 14, "bold"), text_color="#145B06").pack(anchor="w", padx=10, pady=(5,0))
            ctk.CTkLabel(card, text=doc, font=("Arial", 11), text_color="#555555").pack(anchor="w", padx=10, pady=(0,5))

            # Botão de seleção que envia os dados de volta
            btn = ctk.CTkButton(card, text="SELECIONAR", width=100, height=25, font=("Arial", 11, "bold"),
                                fg_color="#2E8B57", hover_color="#1E5D3A",
                                command=lambda c=cli: self.selecionar(c))
            btn.place(relx=0.97, rely=0.5, anchor="e")

    def selecionar(self, cliente):
        """ Fecha a janela e executa a função de preenchimento na tela principal. """
        self.callback(cliente)
        self.destroy()

# =============================================================================
# FUNÇÕES DE FORMATAÇÃO (MÁSCARAS)
# =============================================================================
def aplicar_titulo(e):
    """ Coloca iniciais maiúsculas enquanto o usuário digita. """
    t = e.get().title(); p = e.index("insert"); e.delete(0, "end"); e.insert(0, t); e.icursor(p)

def mascara_cpf(e):
    """ Formata CPF: 000.000.000-00 """
    v = "".join(filter(str.isdigit, e.get()))
    if len(v) <= 3: fmt = v
    elif len(v) <= 6: fmt = f"{v[:3]}.{v[3:]}"
    elif len(v) <= 9: fmt = f"{v[:3]}.{v[3:6]}.{v[6:]}"
    else: fmt = f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:11]}"
    e.delete(0, "end"); e.insert(0, fmt[:14])

def mascara_cnpj(e):
    """ Formata CNPJ: 00.000.000/0000-00 """
    v = "".join(filter(str.isdigit, e.get()))
    if len(v) <= 2: fmt = v
    elif len(v) <= 5: fmt = f"{v[:2]}.{v[2:]}"
    elif len(v) <= 8: fmt = f"{v[:2]}.{v[2:5]}.{v[5:]}"
    elif len(v) <= 12: fmt = f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:]}"
    else: fmt = f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:14]}"
    e.delete(0, "end"); e.insert(0, fmt[:18])

def mascara_cep(e):
    """ Formata CEP: 00.000-000 """
    v = "".join(filter(str.isdigit, e.get()))
    fmt = f"{v[:2]}.{v[2:5]}-{v[5:8]}" if len(v) > 5 else v
    e.delete(0, "end"); e.insert(0, fmt[:10])

def mascara_telefone(e):
    """ Formata Telefone: (00) 00000-0000 """
    v = "".join(filter(str.isdigit, e.get()))
    fmt = f"({v[:2]}) {v[2:7]}-{v[7:11]}" if len(v) > 7 else v
    e.delete(0, "end"); e.insert(0, fmt[:15])

# =============================================================================
# CLASSE: PESSOA FÍSICA (PF)
# =============================================================================
class PessoaFisica(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}          # Dicionário para gerenciar os campos de texto
        self.modo_edicao = False  # Controla se o botão SALVAR vai criar ou atualizar
        self.id_original_cpf = None # Backup do CPF para localizar o registro no banco

    def abrir_fisica(self):
        """ Cria e posiciona todos os elementos da tela de Pessoa Física. """
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")
        
        # Lista de configuração dos campos para criação automática
        campos = [
            ("Nome Completo:", "nome", "Digite o nome...", aplicar_titulo),
            ("CPF:", "cpf", "000.000.000-00", mascara_cpf),
            ("Endereço:", "logradouro", "Rua...", aplicar_titulo),
            ("Número:", "numero", "Nº", None),
            ("Bairro:", "bairro", "Bairro...", aplicar_titulo),
            ("Cidade:", "cidade", "Cidade...", aplicar_titulo),
            ("Estado:", "estado", "UF", aplicar_titulo),
            ("CEP:", "cep", "00.000-000", mascara_cep),
            ("Telefone:", "telefone", "(00) 00000-0000", mascara_telefone),
            ("Email:", "email", "exemplo@email.com", None)
        ]
        
        # Gera os campos na tela usando um loop
        for i, (txt, chave, msg, func) in enumerate(campos):
            ctk.CTkLabel(self, text=txt, font=("Arial", 13, "bold"), text_color="#145B06").grid(row=i, column=0, padx=10, pady=2, sticky="w")
            entry = ctk.CTkEntry(self, width=380, height=30, placeholder_text=msg, fg_color="#F0F0F0", border_width=0, corner_radius=10, text_color="black")
            if func: entry.bind("<KeyRelease>", lambda event, e=entry, f=func: f(e))
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            self.inputs[chave] = entry

        # Botões de controle da interface
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", width=120, fg_color="#2E8B57", hover_color="#145B06", command=self.fluxo_salvamento)
        self.btn_salvar.place(x=130, y=420)
        
        self.btn_buscar = ctk.CTkButton(self, text="BUSCAR", width=120, fg_color="#D2691E", hover_color="#145B06", command=self.iniciar_busca)
        self.btn_buscar.place(x=260, y=420)
        
        self.btn_retornar = ctk.CTkButton(self, text="RETORNAR", width=120, fg_color="#696969", hover_color="#145B06", command=self.resetar_interface)
        
        self.btn_deletar = ctk.CTkButton(self, text="DELETAR", width=120, fg_color="#B22222", hover_color="#145B06", command=self.excluir_pf)

    def iniciar_busca(self):
        """ Pega o nome/CPF e abre a janela de resultados. """
        busca = self.inputs["nome"].get().strip() or self.inputs["cpf"].get().strip()
        if not busca: return messagebox.showwarning("Aviso", "Digite Nome ou CPF!")
        res = database.buscar_clientes_pf_flexivel(busca)
        if res: JanelaBuscaClientes(res, self.preencher_campos, "pf")
        else: messagebox.showinfo("Busca", "Nenhum cliente encontrado.")

    def preencher_campos(self, cliente):
        """ Quando selecionado na busca, carrega os dados nos campos. """
        self.resetar_interface()
        for k, v in cliente.items():
            if k in self.inputs: self.inputs[k].insert(0, str(v) if v else "")
        self.id_original_cpf = cliente['cpf']
        self.modo_edicao = True
        # Gerencia a troca de botões para modo Edição
        self.btn_buscar.place_forget()
        self.btn_retornar.place(x=260, y=420)
        self.btn_deletar.place(x=390, y=420)

    def fluxo_salvamento(self):
        """ Executa a ação de Salvar ou Atualizar no banco. """
        dados = {k: v.get() for k, v in self.inputs.items()}
        if self.modo_edicao:
            database.atualizar_cliente_pf(dados)
            messagebox.showinfo("Sucesso", "Atualizado!")
        else:
            database.salvar_cliente_pf(dados)
            messagebox.showinfo("Sucesso", "Salvo!")
        self.resetar_interface()

    def excluir_pf(self):
        """ Deleta o cliente após confirmação. """
        if messagebox.askyesno("Confirma", "Excluir cliente?"):
            database.deletar_cliente_pf(self.id_original_cpf); self.resetar_interface()

    def resetar_interface(self):
        """ Limpa a tela e volta ao modo de novo cadastro. """
        for e in self.inputs.values(): e.delete(0, 'end')
        self.id_original_cpf = None
        self.modo_edicao = False
        self.btn_deletar.place_forget()
        self.btn_retornar.place_forget()
        self.btn_buscar.place(x=260, y=420)

# =============================================================================
# CLASSE: PESSOA JURÍDICA (PJ)
# =============================================================================
class PessoaJuridica(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inputs = {}
        self.modo_edicao = False
        self.id_original_cnpj = None

    def abrir_juridico(self):
        """ Cria e posiciona todos os elementos da tela de Pessoa Jurídica. """
        self.place(x=0, y=0, relwidth=1, relheight=1); self.configure(fg_color="white")
        
        # Campos específicos para Empresas
        campos_pj = [
            ("Razão Social:", "empresa", "Nome da empresa...", aplicar_titulo),
            ("Nome Fantasia:", "fantasia", "Nome fantasia...", aplicar_titulo),
            ("CNPJ:", "cnpj", "00.000.000/0000-00", mascara_cnpj),
            ("Inscrição:", "inscricao", "Estadual...", None),
            ("Endereço:", "logradouro", "Rua...", aplicar_titulo),
            ("Número:", "numero", "Nº", None),
            ("Bairro:", "bairro", "Bairro...", aplicar_titulo),
            ("Cidade:", "cidade", "Cidade...", aplicar_titulo),
            ("Estado:", "estado", "UF", aplicar_titulo),
            ("CEP:", "cep", "00.000-000", mascara_cep),
            ("Telefone:", "telefone", "(00) 0000-0000", mascara_telefone),
            ("Email:", "email", "email@empresa.com", None)
        ]
        
        for i, (txt, chave, msg, func) in enumerate(campos_pj):
            ctk.CTkLabel(self, text=txt, font=("Arial", 13, "bold"), text_color="#145B06").grid(row=i, column=0, padx=10, pady=2, sticky="w")
            entry = ctk.CTkEntry(self, width=380, height=30, placeholder_text=msg, fg_color="#F0F0F0", border_width=0, corner_radius=10, text_color="black")
            if func: entry.bind("<KeyRelease>", lambda event, e=entry, f=func: f(e))
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            self.inputs[chave] = entry

        # Botões de ação para PJ
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR", width=120, fg_color="#2E8B57", hover_color="#145B06", command=self.fluxo_salvamento)
        self.btn_salvar.place(x=130, y=450)
        self.btn_buscar = ctk.CTkButton(self, text="BUSCAR", width=120, fg_color="#D2691E", hover_color="#145B06", command=self.iniciar_busca)
        self.btn_buscar.place(x=260, y=450)
        self.btn_retornar = ctk.CTkButton(self, text="RETORNAR", width=120, fg_color="#696969", hover_color="#145B06", command=self.resetar_interface)
        self.btn_deletar = ctk.CTkButton(self, text="DELETAR", width=120, fg_color="#B22222", hover_color="#145B06", command=self.excluir_pj)

    def iniciar_busca(self):
        """ Busca empresas por Razão Social ou CNPJ. """
        busca = self.inputs["empresa"].get().strip() or self.inputs["cnpj"].get().strip()
        if not busca: return messagebox.showwarning("Aviso", "Digite Empresa ou CNPJ!")
        res = database.buscar_clientes_pj_flexivel(busca)
        if res: JanelaBuscaClientes(res, self.preencher_campos, "pj")
        else: messagebox.showinfo("Busca", "Nenhuma empresa encontrada.")

    def preencher_campos(self, cliente):
        """ Preenche os dados da empresa para edição. """
        self.resetar_interface()
        for k, v in cliente.items():
            if k in self.inputs: self.inputs[k].insert(0, str(v) if v else "")
        self.id_original_cnpj = cliente['cnpj']
        self.modo_edicao = True
        self.btn_buscar.place_forget()
        self.btn_retornar.place(x=260, y=450)
        self.btn_deletar.place(x=390, y=450)

    def fluxo_salvamento(self):
        """ Decide entre criar nova empresa ou atualizar dados. """
        dados = {k: v.get() for k, v in self.inputs.items()}
        if self.modo_edicao:
            database.atualizar_cliente_pj(dados)
            messagebox.showinfo("Sucesso", "Atualizado!")
        else:
            database.salvar_cliente_pj(dados)
            messagebox.showinfo("Sucesso", "Salvo!")
        self.resetar_interface()

    def excluir_pj(self):
        """ Exclui a empresa do banco. """
        if messagebox.askyesno("Confirma", "Excluir empresa?"):
            database.deletar_cliente_pj(self.id_original_cnpj); self.resetar_interface()

    def resetar_interface(self):
        """ Limpa a tela de PJ. """
        for e in self.inputs.values(): e.delete(0, 'end')
        self.id_original_cnpj = None
        self.modo_edicao = False
        self.btn_deletar.place_forget()
        self.btn_retornar.place_forget()
        self.btn_buscar.place(x=260, y=450)
