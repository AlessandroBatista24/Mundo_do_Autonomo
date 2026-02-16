import sqlite3 # Biblioteca nativa do Python para manipulação de bancos de dados SQL

# --- FUNÇÃO DE CONEXÃO ---
def conectar():
    """Estabelece a conexão com o arquivo do banco de dados."""
    # Se o arquivo não existir, o SQLite o criará automaticamente na pasta do projeto
    return sqlite3.connect("sistema_gestao.db")

# --- CRIAÇÃO ESTRUTURAL (DDL) ---
def criar_banco():
    """Cria todas as tabelas necessárias caso elas ainda não existam."""
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de Clientes Pessoa Física - Uso de UNIQUE no CPF para evitar duplicidade
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes_pf (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        logradouro TEXT NOT NULL,
        numero TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT,
        cep TEXT,
        telefone TEXT NOT NULL,
        email TEXT
    )
    """)

    # Tabela de Clientes Pessoa Jurídica - Estrutura similar à PF com campos empresariais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes_pj (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa TEXT NOT NULL,
        fantasia TEXT,
        cnpj TEXT NOT NULL UNIQUE,
        inscricao TEXT,
        logradouro TEXT NOT NULL,
        numero TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT,
        cep TEXT,
        telefone TEXT NOT NULL,
        email TEXT
    )
    """)

    # Tabela de Produtos - Uso do tipo REAL para permitir cálculos matemáticos precisos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT NOT NULL,
        marca TEXT,
        v_compra REAL NOT NULL,
        imposto REAL DEFAULT 0,
        custo_fixo REAL DEFAULT 0,
        margem_lucro REAL DEFAULT 0,
        quantidade REAL NOT NULL,
        unidade TEXT NOT NULL,
        v_venda REAL NOT NULL
    )
    """)

    # Tabela de Serviços - Focada em custos operacionais e margem de serviço
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        v_custo REAL NOT NULL,
        v_fixo REAL DEFAULT 0,
        v_imposto REAL DEFAULT 0,
        v_margem REAL DEFAULT 0,
        v_final REAL NOT NULL
    )
    """)

    # Tabela de Estoque - Utiliza FOREIGN KEY para vincular ao ID do produto
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estoque (
        id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        qtd_atual REAL NOT NULL,
        qtd_minima REAL DEFAULT 0,
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
    """)

    # Tabela de Orçamentos - O "Mestre" que resume a venda/serviço
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orcamentos (
        id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_cliente TEXT NOT NULL, -- Identifica se o ID pertence a PF ou PJ
        cliente_id INTEGER NOT NULL,
        data_emissao TEXT NOT NULL,
        total_produtos REAL NOT NULL,
        total_servicos REAL NOT NULL,
        valor_geral REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pendente'
    )
    """)

    # Tabela Detalhada de Itens - Permite que um orçamento tenha múltiplos produtos/serviços
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orcamento_itens (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
        id_orcamento INTEGER NOT NULL,
        referencia_id INTEGER NOT NULL, -- ID do Produto ou do Serviço
        tipo_item TEXT NOT NULL,        -- Define se a referência é 'Produto' ou 'Serviço'
        quantidade REAL NOT NULL,
        valor_unitario REAL NOT NULL,
        valor_total_item REAL NOT NULL,
        FOREIGN KEY (id_orcamento) REFERENCES orcamentos (id_orcamento)
    )
    """)

    # Tabelas Financeiras Desmembradas para facilitar relatórios individuais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas_pagar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data_vencimento TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pendente'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas_receber (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origem_orcamento_id INTEGER,
        valor REAL NOT NULL,
        data_vencimento TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pendente',
        FOREIGN KEY (origem_orcamento_id) REFERENCES orcamentos (id_orcamento)
    )
    """)

    # Tabela de Caixa - Onde ocorre a consolidação real do fluxo financeiro
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS caixa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_movimentacao TEXT NOT NULL,
        tipo TEXT NOT NULL, -- 'Entrada' ou 'Saída'
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        saldo_momento REAL NOT NULL,
        origem_id TEXT -- Chave de rastreabilidade para auditoria
    )
    """)

    conn.commit() # Salva todas as alterações estruturais
    conn.close()  # Fecha a conexão para liberar o arquivo

# --- BLOCO DE EXECUÇÃO INICIAL ---
if __name__ == "__main__":
    criar_banco()
    print("Banco de Dados e todas as Tabelas (PF/PJ/Financeiro) criados com sucesso!")

# --- FUNÇÕES DE INSERÇÃO (DML) ---

def salvar_cliente_pf(dados):
    """Insere dados de Pessoa Física usando Named Placeholders (:nome) para segurança."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes_pf (nome, cpf, logradouro, numero, bairro, cidade, estado, cep, telefone, email)
        VALUES (:nome, :cpf, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)
    """, dados)
    conn.commit()
    conn.close()

def salvar_cliente_pj(dados):
    """Insere dados de Pessoa Jurídica diretamente do dicionário da interface."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes_pj (empresa, fantasia, cnpj, inscricao, logradouro, numero, bairro, cidade, estado, cep, telefone, email)
        VALUES (:empresa, :fantasia, :cnpj, :inscricao, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)
    """, dados)
    conn.commit()
    conn.close()

def salvar_produto(dados):
    """Converte strings da UI em números reais e salva na tabela de produtos."""
    conn = conectar()
    cursor = conn.cursor()
    
    # .copy() evita alterar o dicionário original da interface durante o tratamento
    d = dados.copy()
    # Limpeza de strings monetárias (Ex: "R$ 1.200,50" -> 1200.50)
    d['v_compra'] = float(d['v_compra'].replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_venda'] = float(d['v_venda'].replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    # Conversão de percentuais e quantidades para float
    d['imposto'] = float(d['imposto'].replace(",", ".") or 0)
    d['custo_fixo'] = float(d['custo_fixo'].replace(",", ".") or 0)
    d['margem_lucro'] = float(d['margem_lucro'].replace(",", ".") or 0)
    d['quantidade'] = float(d['quantidade'].replace(",", ".") or 0)

    cursor.execute("""
        INSERT INTO produtos (produto, marca, v_compra, imposto, custo_fixo, margem_lucro, quantidade, unidade, v_venda)
        VALUES (:produto, :marca, :v_compra, :imposto, :custo_fixo, :margem_lucro, :quantidade, :unidade, :v_venda)
    """, d)
    conn.commit()
    conn.close()

def salvar_servico(dados):
    """Realiza o tratamento numérico e salva o cadastro de novos serviços."""
    conn = conectar()
    cursor = conn.cursor()
    
    d = dados.copy()
    d['v_custo'] = float(d['v_custo'].replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_final'] = float(d['v_final'].replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    d['v_fixo'] = float(d['v_fixo'].replace(",", ".") or 0)
    d['v_imposto'] = float(d['v_imposto'].replace(",", ".") or 0)
    d['v_margem'] = float(d['v_margem'].replace(",", ".") or 0)

    cursor.execute("""
        INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final)
        VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)
    """, d)
    conn.commit()
    conn.close()
