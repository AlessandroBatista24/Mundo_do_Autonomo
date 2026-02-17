import sqlite3 # Importa o módulo nativo para trabalhar com banco de dados SQLite

# Função para estabelecer conexão com o arquivo do banco de dados
def conectar():
    return sqlite3.connect("sistema_gestao.db")

# Função responsável por criar a estrutura inicial do sistema (Tabelas)
def criar_banco():
    conn = conectar(); cursor = conn.cursor() # Abre conexão e cria um cursor para executar comandos SQL
    
    # Criação da Tabela de Clientes Pessoa Física (PF) se ela não existir
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes_pf (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cpf TEXT NOT NULL UNIQUE,
        logradouro TEXT NOT NULL, numero TEXT, bairro TEXT, cidade TEXT, estado TEXT,
        cep TEXT, telefone TEXT NOT NULL, email TEXT)""")

    # Criação da Tabela de Clientes Pessoa Jurídica (PJ) se ela não existir
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes_pj (
        id INTEGER PRIMARY KEY AUTOINCREMENT, empresa TEXT NOT NULL, fantasia TEXT,
        cnpj TEXT NOT NULL UNIQUE, inscricao TEXT, logradouro TEXT NOT NULL,
        numero TEXT, bairro TEXT, cidade TEXT, estado TEXT, cep TEXT,
        telefone TEXT NOT NULL, email TEXT)""")

    # Criação da Tabela de Produtos com campos para formação de preço
    cursor.execute("""CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, fabricante TEXT NOT NULL,
        v_compra REAL NOT NULL, imposto REAL DEFAULT 0, custo_fixo REAL DEFAULT 0,
        margem_lucro REAL DEFAULT 0, quantidade REAL NOT NULL, unidade TEXT NOT NULL, v_venda REAL NOT NULL)""")

    # Criação da Tabela de Serviços
    cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL,
        v_custo REAL NOT NULL, v_fixo REAL DEFAULT 0, v_imposto REAL DEFAULT 0,
        v_margem REAL DEFAULT 0, v_final REAL NOT NULL)""")

    # Criação das tabelas auxiliares: Estoque, Orçamentos, Itens de Orçamento, Contas e Fluxo de Caixa
    cursor.execute("CREATE TABLE IF NOT EXISTS estoque (id_estoque INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER, qtd_atual REAL, qtd_minima REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS orcamentos (id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT, tipo_cliente TEXT, cliente_id INTEGER, data_emissao TEXT, total_produtos REAL, total_servicos REAL, valor_geral REAL, status TEXT DEFAULT 'Pendente')")
    cursor.execute("CREATE TABLE IF NOT EXISTS orcamento_itens (id_item INTEGER PRIMARY KEY AUTOINCREMENT, id_orcamento INTEGER, referencia_id INTEGER, tipo_item TEXT, quantidade REAL, valor_unitario REAL, valor_total_item REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS contas_pagar (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT, valor REAL, data_vencimento TEXT, status TEXT DEFAULT 'Pendente')")
    cursor.execute("CREATE TABLE IF NOT EXISTS contas_receber (id INTEGER PRIMARY KEY AUTOINCREMENT, origem_orcamento_id INTEGER, valor REAL, data_vencimento TEXT, status TEXT DEFAULT 'Pendente')")
    cursor.execute("CREATE TABLE IF NOT EXISTS caixa (id INTEGER PRIMARY KEY AUTOINCREMENT, data_movimentacao TEXT, tipo TEXT, descricao TEXT, valor REAL, saldo_momento REAL, origem_id TEXT)")

    conn.commit(); conn.close() # Salva as alterações (commit) e fecha a conexão

# Função para limpar strings (R$, %, vírgulas) e converter para float antes de salvar no banco
def tratar_numericos(dicionario, campos):
    for campo in campos:
        if campo in dicionario:
            # Remove símbolos e espaços, substitui ponto por nada e vírgula por ponto (padrão americano/programação)
            val = str(dicionario[campo]).replace("R$", "").replace(" ", "").replace("%", "").strip()
            if "," in val: val = val.replace(".", "").replace(",", ".")
            try: dicionario[campo] = float(val or 0) # Tenta converter, se vazio ou erro, define como 0.0
            except: dicionario[campo] = 0.0
    return dicionario

# --- Módulo de PRODUTOS ---

# Insere um novo produto validando se ele já existe (nome + fabricante)
def salvar_produto(dados):
    conn = conectar(); cursor = conn.cursor()
    d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
    cursor.execute("SELECT id FROM produtos WHERE produto = ? AND fabricante = ?", (d['produto'], d['fabricante']))
    if cursor.fetchone(): conn.close(); return False # Retorna Falso se o produto já existir
    cursor.execute("INSERT INTO produtos (produto, fabricante, v_compra, imposto, custo_fixo, margem_lucro, quantidade, unidade, v_venda) VALUES (:produto, :fabricante, :v_compra, :imposto, :custo_fixo, :margem_lucro, :quantidade, :unidade, :v_venda)", d)
    conn.commit(); conn.close(); return True

# Busca produtos usando o operador LIKE (busca parcial por nome ou fabricante)
def buscar_produtos_flexivel(termo):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor() # Row_factory permite acessar colunas pelo nome
    cursor.execute("SELECT * FROM produtos WHERE produto LIKE ? OR fabricante LIKE ?", (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res # Converte os resultados em uma lista de dicionários

# Atualiza dados de um produto existente usando o nome e fabricante original como chave
def atualizar_produto_composto(dados, p_orig, f_orig):
    conn = conectar(); cursor = conn.cursor()
    d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
    d.update({'p_orig': p_orig, 'f_orig': f_orig}) # Adiciona as chaves originais ao dicionário para o WHERE
    cursor.execute("UPDATE produtos SET produto=:produto, fabricante=:fabricante, v_compra=:v_compra, imposto=:imposto, custo_fixo=:custo_fixo, margem_lucro=:margem_lucro, quantidade=:quantidade, unidade=:unidade, v_venda=:v_venda WHERE produto=:p_orig AND fabricante=:f_orig", d)
    conn.commit(); conn.close()

# Deleta um produto baseado na combinação de nome e fabricante
def deletar_produto_composto(p, f):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE produto = ? AND fabricante = ?", (p, f))
    conn.commit(); conn.close()

# --- Módulo de CLIENTES PF ---

# Salva um novo cliente Pessoa Física
def salvar_cliente_pf(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes_pf (nome, cpf, logradouro, numero, bairro, cidade, estado, cep, telefone, email) VALUES (:nome, :cpf, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)", dados)
    conn.commit(); conn.close()

# Busca flexível para Clientes PF (por nome ou CPF)
def buscar_clientes_pf_flexivel(termo):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes_pf WHERE nome LIKE ? OR cpf LIKE ?", (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

# Atualiza informações do cliente PF tendo o CPF como identificador único
def atualizar_cliente_pf(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE clientes_pf SET nome=:nome, logradouro=:logradouro, numero=:numero, bairro=:bairro, cidade=:cidade, estado=:estado, cep=:cep, telefone=:telefone, email=:email WHERE cpf=:cpf", dados)
    conn.commit(); conn.close()

# Remove um cliente PF pelo CPF
def deletar_cliente_pf(cpf):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes_pf WHERE cpf = ?", (cpf,))
    conn.commit(); conn.close()

# --- Módulo de CLIENTES PJ ---

# Salva um novo cliente Pessoa Jurídica
def salvar_cliente_pj(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes_pj (empresa, fantasia, cnpj, inscricao, logradouro, numero, bairro, cidade, estado, cep, telefone, email) VALUES (:empresa, :fantasia, :cnpj, :inscricao, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)", dados)
    conn.commit(); conn.close()

# Busca flexível para Clientes PJ (por Razão Social, Nome Fantasia ou CNPJ)
def buscar_clientes_pj_flexivel(termo):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes_pj WHERE empresa LIKE ? OR fantasia LIKE ? OR cnpj LIKE ?", (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

# Atualiza informações da empresa usando o CNPJ como identificador
def atualizar_cliente_pj(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE clientes_pj SET empresa=:empresa, fantasia=:fantasia, inscricao=:inscricao, logradouro=:logradouro, numero=:numero, bairro=:bairro, cidade=:cidade, estado=:estado, cep=:cep, telefone=:telefone, email=:email WHERE cnpj=:cnpj", dados)
    conn.commit(); conn.close()

# Remove um cliente PJ pelo CNPJ
def deletar_cliente_pj(cnpj):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes_pj WHERE cnpj = ?", (cnpj,))
    conn.commit(); conn.close()

# --- Módulo de SERVIÇOS ---

# Salva um novo serviço, tratando os campos numéricos (preço/custo)
def salvar_servico(dados):
    conn = conectar(); cursor = conn.cursor()
    d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
    cursor.execute("INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final) VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)", d)
    conn.commit(); conn.close()

# Busca serviços por descrição
def buscar_servicos_flexivel(termo):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos WHERE descricao LIKE ?", (f"%{termo}%",))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

# Atualiza um serviço existente (Nota: o código enviado parece estar cortado ao final)
def atualizar_servico_com_desc(dados, desc_orig):
    conn = conectar(); cursor = conn.cursor()
    d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
    # d.update({'desc_orig': desc_orig}) ... (Continuação lógica do código)
