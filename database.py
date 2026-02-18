import sqlite3

# Estabelece a conexão com o arquivo do banco de dados SQLite
def conectar():
    return sqlite3.connect("sistema_gestao.db")

# Função responsável por criar a estrutura inicial do sistema (Tabelas)
def criar_banco():
    conn = conectar(); cursor = conn.cursor()
    
    # 1. Clientes Pessoa Física: Armazena dados pessoais e contato
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes_pf (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cpf TEXT NOT NULL UNIQUE,
        logradouro TEXT NOT NULL, numero TEXT, bairro TEXT, cidade TEXT, estado TEXT,
        cep TEXT, telefone TEXT NOT NULL, email TEXT)""")
    
    # 2. Clientes Pessoa Jurídica: Foco em dados empresariais e CNPJ
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes_pj (
        id INTEGER PRIMARY KEY AUTOINCREMENT, empresa TEXT NOT NULL, fantasia TEXT,
        cnpj TEXT NOT NULL UNIQUE, inscricao TEXT, logradouro TEXT NOT NULL,
        numero TEXT, bairro TEXT, cidade TEXT, estado TEXT, cep TEXT,
        telefone TEXT NOT NULL, email TEXT)""")
    
    # 3. Cabeçalho de Orçamentos: Centraliza os totais e dados do cliente no momento da venda
    cursor.execute("""CREATE TABLE IF NOT EXISTS orcamentos (
        id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT, tipo_cliente TEXT, cliente_id INTEGER, 
        nome_cliente TEXT, documento TEXT, endereco_completo TEXT, data_emissao TEXT, 
        validade_dias INTEGER, total_produtos REAL, total_servicos REAL, 
        valor_geral REAL, status TEXT DEFAULT 'Pendente')""")
    
    # 4. Cadastro de Produtos: REAL é usado para garantir cálculos decimais precisos
    cursor.execute("""CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, fabricante TEXT NOT NULL,
        v_compra REAL NOT NULL, imposto REAL DEFAULT 0, custo_fixo REAL DEFAULT 0,
        margem_lucro REAL DEFAULT 0, quantidade REAL NOT NULL, unidade TEXT NOT NULL, v_venda REAL NOT NULL)""")
    
    # 5. Cadastro de Serviços: Focado em mão de obra e precificação
    cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL,
        v_custo REAL NOT NULL, v_fixo REAL DEFAULT 0, v_imposto REAL DEFAULT 0,
        v_margem REAL DEFAULT 0, v_final REAL NOT NULL)""")
    
    # 6. Tabelas Auxiliares: Controle de estoque e detalhamento dos itens de cada orçamento
    cursor.execute("CREATE TABLE IF NOT EXISTS estoque (id_estoque INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER, qtd_atual REAL, qtd_minima REAL)")
    
    # Itens do Orçamento: Vincula produtos/serviços ao ID de um orçamento pai
    cursor.execute("""CREATE TABLE IF NOT EXISTS orcamento_itens (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT, id_orcamento INTEGER, 
        referencia_id INTEGER, tipo_item TEXT, quantidade REAL, 
        valor_unitario REAL, valor_total_item REAL)""")
    
    conn.commit(); conn.close()

# --- UTILITÁRIOS DE LIMPEZA (ESSENCIAL PARA EVITAR ERROS DECIMAIS) ---
# Esta função higieniza strings vindas da interface (R$, vírgulas, espaços) 
# convertendo-as em floats puros que o banco de dados entende sem multiplicar valores.
def tratar_numericos(dicionario, campos):
    for campo in campos:
        if campo in dicionario:
            # Remove símbolos monetários e espaços para isolar o número
            val = str(dicionario[campo]).replace("R$", "").replace(" ", "").replace("%", "").strip()
            # Converte padrão brasileiro (1.000,00) para padrão computacional (1000.00)
            if "," in val: 
                val = val.replace(".", "").replace(",", ".")
            try: 
                dicionario[campo] = float(val or 0)
            except: 
                dicionario[campo] = 0.0
    return dicionario

# --- MÓDULO CLIENTES PF ---
def salvar_cliente_pf(dados):
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO clientes_pf (nome, cpf, logradouro, numero, bairro, cidade, estado, cep, telefone, email) 
            VALUES (:nome, :cpf, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)""", dados)
        conn.commit(); return True
    except: return False
    finally: conn.close()

def atualizar_cliente_pf(dados):
    conn = conectar(); cursor = conn.cursor()
    # Atualiza registro baseado no CPF (Chave única)
    cursor.execute("""UPDATE clientes_pf SET nome=:nome, logradouro=:logradouro, numero=:numero, 
                      bairro=:bairro, cidade=:cidade, estado=:estado, cep=:cep, 
                      telefone=:telefone, email=:email WHERE cpf=:cpf""", dados)
    conn.commit(); conn.close()

# --- MÓDULO PRODUTOS ---
def salvar_produto(dados):
    conn = conectar(); cursor = conn.cursor()
    try:
        # Aplica a limpeza nos dados antes de enviar ao INSERT
        d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
        cursor.execute("""INSERT INTO produtos (produto, fabricante, v_compra, imposto, custo_fixo, margem_lucro, quantidade, unidade, v_venda) 
            VALUES (:produto, :fabricante, :v_compra, :imposto, :custo_fixo, :margem_lucro, :quantidade, :unidade, :v_venda)""", d)
        conn.commit(); return True
    except: return False
    finally: conn.close()
# Atualiza um produto existente usando Nome e Fabricante como chave de busca (Chave Composta)
def atualizar_produto_composto(dados, p_orig, f_orig):
    conn = conectar(); cursor = conn.cursor()
    # Limpa os dados numéricos antes da atualização para evitar erros de ponto flutuante
    d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
    # Adiciona os valores originais ao dicionário para localizar o registro correto no WHERE
    d.update({'p_orig': p_orig, 'f_orig': f_orig})
    cursor.execute("""UPDATE produtos SET produto=:produto, fabricante=:fabricante, v_compra=:v_compra, imposto=:imposto, 
                      custo_fixo=:custo_fixo, margem_lucro=:margem_lucro, quantidade=:quantidade, unidade=:unidade, 
                      v_venda=:v_venda WHERE produto=:p_orig AND fabricante=:f_orig""", d)
    conn.commit(); conn.close()

# Remove um produto do banco baseado na combinação única de nome e fabricante
def deletar_produto_composto(p, f):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE produto = ? AND fabricante = ?", (p, f))
    conn.commit(); conn.close()

# Realiza busca por nome de produto ou fabricante usando o operador LIKE (busca parcial)
def buscar_produtos_flexivel(termo):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE produto LIKE ? OR fabricante LIKE ?", (f"%{termo}%", f"%{termo}%"))
    # Converte os resultados em uma lista de dicionários para fácil manipulação na interface
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

# --- MÓDULO SERVIÇOS ---

# Insere um novo serviço aplicando o tratamento de strings para números
def salvar_servico(dados):
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
        cursor.execute("""INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final) 
            VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)""", d)
        conn.commit(); return True
    except: return False
    finally: conn.close()

# Atualiza serviço usando a descrição original para identificar o registro
def atualizar_servico_com_desc(dados, desc_orig):
    conn = conectar(); cursor = conn.cursor()
    d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
    d['desc_orig'] = desc_orig
    cursor.execute("""UPDATE servicos SET descricao=:descricao, v_custo=:v_custo, v_fixo=:v_fixo, 
                      v_imposto=:v_imposto, v_margem=:v_margem, v_final=:v_final 
                      WHERE descricao=:desc_orig""", d)
    conn.commit(); conn.close()

# Busca serviços por descrição
def buscar_servicos_flexivel(termo):
    conn = conectar(); conn.row_factory = sqlite3.Row; cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos WHERE descricao LIKE ?", (f"%{termo}%",))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

# --- MÓDULO ORÇAMENTOS (LÓGICA MESTRE/DETALHE) ---

# Esta função salva o orçamento e seus itens em duas tabelas diferentes de forma vinculada
def salvar_orcamento_completo(dados_h, lista_i):
    conn = conectar(); cursor = conn.cursor()
    try:
        # 1. Salva o cabeçalho (dados gerais do cliente e totais)
        cursor.execute("""INSERT INTO orcamentos (tipo_cliente, cliente_id, nome_cliente, documento, endereco_completo, data_emissao, validade_dias, total_produtos, total_servicos, valor_geral, status) 
            VALUES (:tipo_cliente, :cliente_id, :nome_cliente, :documento, :endereco_completo, :data_emissao, :validade_dias, :total_produtos, :total_servicos, :valor_geral, :status)""", dados_h)
        
        # 2. Recupera o ID gerado automaticamente para este orçamento (Chave Estrangeira)
        id_orc = cursor.lastrowid
        
        # 3. Percorre a lista de itens do carrinho e salva um por um vinculando ao ID acima
        for item in lista_i:
            cursor.execute("""INSERT INTO orcamento_itens (id_orcamento, referencia_id, tipo_item, quantidade, valor_unitario, valor_total_item) 
                VALUES (?, ?, ?, ?, ?, ?)""", (id_orc, item['id'], item['tipo'], item['qtd'], item['valor'], item['total']))
        
        conn.commit(); return True
    except Exception as e:
        # Em caso de erro, desfaz qualquer inserção parcial (Rollback)
        print(f"Erro no banco: {e}"); conn.rollback(); return False
    finally: conn.close()
