import sqlite3

# --- FUNÇÃO DE CONEXÃO ---
def conectar():
    return sqlite3.connect("sistema_gestao.db")

# --- CRIAÇÃO ESTRUTURAL (DDL) ---
def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Tabelas de Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes_pf (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cpf TEXT NOT NULL UNIQUE,
        logradouro TEXT NOT NULL, numero TEXT, bairro TEXT, cidade TEXT, estado TEXT,
        cep TEXT, telefone TEXT NOT NULL, email TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes_pj (
        id INTEGER PRIMARY KEY AUTOINCREMENT, empresa TEXT NOT NULL, fantasia TEXT,
        cnpj TEXT NOT NULL UNIQUE, inscricao TEXT, logradouro TEXT NOT NULL,
        numero TEXT, bairro TEXT, cidade TEXT, estado TEXT, cep TEXT,
        telefone TEXT NOT NULL, email TEXT
    )""")

    # Tabela de Produtos e Serviços
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL UNIQUE, marca TEXT,
        v_compra REAL NOT NULL, imposto REAL DEFAULT 0, custo_fixo REAL DEFAULT 0,
        margem_lucro REAL DEFAULT 0, quantidade REAL NOT NULL, unidade TEXT NOT NULL, v_venda REAL NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL UNIQUE,
        v_custo REAL NOT NULL, v_fixo REAL DEFAULT 0, v_imposto REAL DEFAULT 0,
        v_margem REAL DEFAULT 0, v_final REAL NOT NULL
    )""")

    # Tabelas de Estoque e Orçamentos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estoque (
        id_estoque INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER NOT NULL,
        qtd_atual REAL NOT NULL, qtd_minima REAL DEFAULT 0,
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orcamentos (
        id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT, tipo_cliente TEXT NOT NULL,
        cliente_id INTEGER NOT NULL, data_emissao TEXT NOT NULL, total_produtos REAL NOT NULL,
        total_servicos REAL NOT NULL, valor_geral REAL NOT NULL, status TEXT NOT NULL DEFAULT 'Pendente'
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orcamento_itens (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT, id_orcamento INTEGER NOT NULL,
        referencia_id INTEGER NOT NULL, tipo_item TEXT NOT NULL, quantidade REAL NOT NULL,
        valor_unitario REAL NOT NULL, valor_total_item REAL NOT NULL,
        FOREIGN KEY (id_orcamento) REFERENCES orcamentos (id_orcamento)
    )""")

    # Tabelas Financeiras
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas_pagar (
        id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL, valor REAL NOT NULL,
        data_vencimento TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pendente'
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas_receber (
        id INTEGER PRIMARY KEY AUTOINCREMENT, origem_orcamento_id INTEGER,
        valor REAL NOT NULL, data_vencimento TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pendente',
        FOREIGN KEY (origem_orcamento_id) REFERENCES orcamentos (id_orcamento)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS caixa (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_movimentacao TEXT NOT NULL,
        tipo TEXT NOT NULL, descricao TEXT NOT NULL, valor REAL NOT NULL,
        saldo_momento REAL NOT NULL, origem_id TEXT
    )""")

    conn.commit()
    conn.close()

# --- FUNÇÕES DE SALVAMENTO (PF / PJ / PRODUTOS / SERVIÇOS) ---

def salvar_cliente_pf(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes_pf (nome, cpf, logradouro, numero, bairro, cidade, estado, cep, telefone, email) VALUES (:nome, :cpf, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)", dados)
    conn.commit(); conn.close()

def salvar_cliente_pj(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes_pj (empresa, fantasia, cnpj, inscricao, logradouro, numero, bairro, cidade, estado, cep, telefone, email) VALUES (:empresa, :fantasia, :cnpj, :inscricao, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)", dados)
    conn.commit(); conn.close()

def salvar_produto(dados):
    conn = conectar(); cursor = conn.cursor()
    d = dados.copy()
    d['v_compra'] = float(str(d['v_compra']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_venda'] = float(str(d['v_venda']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    cursor.execute("INSERT INTO produtos (produto, marca, v_compra, imposto, custo_fixo, margem_lucro, quantidade, unidade, v_venda) VALUES (:produto, :marca, :v_compra, :imposto, :custo_fixo, :margem_lucro, :quantidade, :unidade, :v_venda)", d)
    conn.commit(); conn.close()

def salvar_servico(dados):
    conn = conectar(); cursor = conn.cursor()
    d = dados.copy()
    d['v_custo'] = float(str(d['v_custo']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_final'] = float(str(d['v_final']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    cursor.execute("INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final) VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)", d)
    conn.commit(); conn.close()

# --- FUNÇÕES DE BUSCA, ATUALIZAÇÃO E EXCLUSÃO ---

# Pessoa Física
def buscar_cliente_pf_por_cpf(cpf):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes_pf WHERE cpf = ?", (cpf,))
    linha = cursor.fetchone(); conn.close()
    return dict(linha) if linha else None

def atualizar_cliente_pf(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE clientes_pf SET nome=:nome, logradouro=:logradouro, numero=:numero, bairro=:bairro, cidade=:cidade, estado=:estado, cep=:cep, telefone=:telefone, email=:email WHERE cpf=:cpf", dados)
    conn.commit(); conn.close()

def deletar_cliente_pf(cpf):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes_pf WHERE cpf = ?", (cpf,))
    conn.commit(); conn.close()

# Pessoa Jurídica
def buscar_cliente_pj_por_cnpj(cnpj):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes_pj WHERE cnpj = ?", (cnpj,))
    linha = cursor.fetchone(); conn.close()
    return dict(linha) if linha else None

def atualizar_cliente_pj(dados):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE clientes_pj SET empresa=:empresa, fantasia=:fantasia, inscricao=:inscricao, logradouro=:logradouro, numero=:numero, bairro=:bairro, cidade=:cidade, estado=:estado, cep=:cep, telefone=:telefone, email=:email WHERE cnpj=:cnpj", dados)
    conn.commit(); conn.close()

def deletar_cliente_pj(cnpj):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes_pj WHERE cnpj = ?", (cnpj,))
    conn.commit(); conn.close()

# Produtos
def buscar_produto_por_nome(nome):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE produto = ?", (nome,))
    linha = cursor.fetchone(); conn.close()
    return dict(linha) if linha else None

def atualizar_produto(dados):
    conn = conectar(); cursor = conn.cursor()
    d = dados.copy()
    d['v_compra'] = float(str(d['v_compra']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_venda'] = float(str(d['v_venda']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    cursor.execute("UPDATE produtos SET marca=:marca, v_compra=:v_compra, imposto=:imposto, custo_fixo=:custo_fixo, margem_lucro=:margem_lucro, quantidade=:quantidade, unidade=:unidade, v_venda=:v_venda WHERE produto=:produto", d)
    conn.commit(); conn.close()

def deletar_produto(nome):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE produto = ?", (nome,))
    conn.commit(); conn.close()

# Serviços
def buscar_servico_por_descricao(desc):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos WHERE descricao = ?", (desc,))
    linha = cursor.fetchone(); conn.close()
    return dict(linha) if linha else None

def atualizar_servico(dados):
    conn = conectar(); cursor = conn.cursor()
    d = dados.copy()
    d['v_custo'] = float(str(d['v_custo']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_final'] = float(str(d['v_final']).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    cursor.execute("UPDATE servicos SET v_custo=:v_custo, v_fixo=:v_fixo, v_imposto=:v_imposto, v_margem=:v_margem, v_final=:v_final WHERE descricao=:descricao", d)
    conn.commit(); conn.close()

def deletar_servico(desc):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM servicos WHERE descricao = ?", (desc,))
    conn.commit(); conn.close()

if __name__ == "__main__":
    criar_banco()
    print("Banco de Dados 100% atualizado!")
