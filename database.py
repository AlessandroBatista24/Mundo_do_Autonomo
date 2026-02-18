import sqlite3
from datetime import datetime

# 1. FUNÇÃO DE CONEXÃO (ESSENCIAL VIR PRIMEIRO)
def conectar():
    """ Estabelece a conexão com o arquivo do banco de dados SQLite """
    conn = sqlite3.connect("sistema_gestao.db")
    conn.row_factory = sqlite3.Row # Permite acessar colunas pelo nome (ex: cliente['nome'])
    return conn

# 2. CRIAÇÃO DO BANCO DE DADOS E TODAS AS TABELAS
def criar_banco():
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # CLIENTES PF
        cursor.execute("""CREATE TABLE IF NOT EXISTS clientes_pf (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cpf TEXT NOT NULL UNIQUE,
            logradouro TEXT NOT NULL, numero TEXT, bairro TEXT, cidade TEXT, estado TEXT,
            cep TEXT, telefone TEXT NOT NULL, email TEXT)""")
        
        # CLIENTES PJ
        cursor.execute("""CREATE TABLE IF NOT EXISTS clientes_pj (
            id INTEGER PRIMARY KEY AUTOINCREMENT, empresa TEXT NOT NULL, fantasia TEXT,
            cnpj TEXT NOT NULL UNIQUE, inscricao TEXT, logradouro TEXT NOT NULL,
            numero TEXT, bairro TEXT, cidade TEXT, estado TEXT, cep TEXT,
            telefone TEXT NOT NULL, email TEXT)""")

        # ORDENS DE SERVIÇO (MESTRE)
        cursor.execute("""CREATE TABLE IF NOT EXISTS ordens_servico (
            id_os INTEGER PRIMARY KEY AUTOINCREMENT, tipo_cliente TEXT, cliente_id INTEGER, 
            nome_cliente TEXT, documento TEXT, endereco_completo TEXT, data_emissao TEXT, 
            data_aprovacao TEXT, total_produtos REAL, total_servicos REAL, 
            valor_geral REAL, status TEXT DEFAULT 'Em Execução')""")

        # ITENS DA O.S. (DETALHE)
        cursor.execute("""CREATE TABLE IF NOT EXISTS os_itens (
            id_item_os INTEGER PRIMARY KEY AUTOINCREMENT, id_os INTEGER, 
            referencia_id INTEGER, tipo_item TEXT, quantidade REAL, 
            valor_unitario REAL, valor_total_item REAL)""")

        # ORÇAMENTOS (CABEÇALHO)
        cursor.execute("""CREATE TABLE IF NOT EXISTS orcamentos (
            id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT, tipo_cliente TEXT, cliente_id INTEGER, 
            nome_cliente TEXT, documento TEXT, endereco_completo TEXT, data_emissao TEXT, 
            validade_dias INTEGER, total_produtos REAL, total_servicos REAL, 
            valor_geral REAL, status TEXT DEFAULT 'Pendente')""")
        
        # PRODUTOS
        cursor.execute("""CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, fabricante TEXT NOT NULL,
            v_compra REAL NOT NULL, imposto REAL DEFAULT 0, custo_fixo REAL DEFAULT 0,
            margem_lucro REAL DEFAULT 0, quantidade REAL NOT NULL, unidade TEXT NOT NULL, v_venda REAL NOT NULL)""")
        
        # SERVIÇOS
        cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL,
            v_custo REAL NOT NULL, v_fixo REAL DEFAULT 0, v_imposto REAL DEFAULT 0,
            v_margem REAL DEFAULT 0, v_final REAL NOT NULL)""")

        # ESTOQUE E ITENS DE ORÇAMENTO
        cursor.execute("CREATE TABLE IF NOT EXISTS estoque (id_estoque INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER, qtd_atual REAL, qtd_minima REAL)")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS orcamento_itens (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT, id_orcamento INTEGER, 
            referencia_id INTEGER, tipo_item TEXT, quantidade REAL, 
            valor_unitario REAL, valor_total_item REAL)""")
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao iniciar banco: {e}")

# --- UTILITÁRIO DE LIMPEZA NUMÉRICA ---
def tratar_numericos(dicionario, campos):
    for campo in campos:
        if campo in dicionario:
            val = str(dicionario[campo]).replace("R$", "").replace(" ", "").replace("%", "").strip()
            if "," in val: 
                val = val.replace(".", "").replace(",", ".")
            try: 
                dicionario[campo] = float(val or 0)
            except: 
                dicionario[campo] = 0.0
    return dicionario
# --- MÓDULO CLIENTES PESSOA FÍSICA (PF) ---

def salvar_cliente_pf(dados):
    """ Insere um novo cliente PF no banco de dados """
    conn = conectar(); cursor = conn.cursor()
    try:
        # CORREÇÃO: 'cidade' em vez de 'city' para bater com a tabela
        cursor.execute("""INSERT INTO clientes_pf (nome, cpf, logradouro, numero, bairro, cidade, estado, cep, telefone, email) 
            VALUES (:nome, :cpf, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)""", dados)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar PF: {e}"); return False
    finally: conn.close()

def atualizar_cliente_pf(dados):
    """ Atualiza dados do cliente baseado no CPF """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE clientes_pf SET nome=:nome, logradouro=:logradouro, numero=:numero, 
                          bairro=:bairro, cidade=:cidade, estado=:estado, cep=:cep, 
                          telefone=:telefone, email=:email WHERE cpf=:cpf""", dados)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao atualizar PF: {e}"); return False
    finally: conn.close()

def deletar_cliente_pf(cpf):
    """ Remove um cliente PF pelo CPF """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes_pf WHERE cpf = ?", (cpf,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True se deletou alguém
    except Exception as e:
        print(f"Erro ao deletar PF: {e}"); return False
    finally: conn.close()

# --- MÓDULO CLIENTES PESSOA JURÍDICA (PJ) ---

def salvar_cliente_pj(dados):
    """ Insere um novo cliente PJ no banco de dados """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO clientes_pj (empresa, fantasia, cnpj, inscricao, logradouro, numero, bairro, cidade, estado, cep, telefone, email) 
            VALUES (:empresa, :fantasia, :cnpj, :inscricao, :logradouro, :numero, :bairro, :cidade, :estado, :cep, :telefone, :email)""", dados)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar PJ: {e}"); return False
    finally: conn.close()

def deletar_cliente_pj(cnpj):
    """ Remove um cliente PJ pelo CNPJ """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes_pj WHERE cnpj = ?", (cnpj,))
        conn.commit(); return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar PJ: {e}"); return False
    finally: conn.close()

# --- MÓDULO PRODUTOS ---

def salvar_produto(dados):
    """ Salva produto com tratamento numérico """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
        cursor.execute("""INSERT INTO produtos (produto, fabricante, v_compra, imposto, custo_fixo, margem_lucro, quantidade, unidade, v_venda) 
            VALUES (:produto, :fabricante, :v_compra, :imposto, :custo_fixo, :margem_lucro, :quantidade, :unidade, :v_venda)""", d)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar Produto: {e}"); return False
    finally: conn.close()

def deletar_produto_composto(p, f):
    """ Remove produto pela chave composta Nome + Fabricante """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM produtos WHERE produto = ? AND fabricante = ?", (p, f))
        conn.commit(); return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar Produto: {e}"); return False
    finally: conn.close()

# --- MÓDULO SERVIÇOS ---

def salvar_servico(dados):
    """ Salva serviço com tratamento numérico """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
        cursor.execute("""INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final) 
            VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)""", d)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar Serviço: {e}"); return False
    finally: conn.close()
# --- MÓDULO DE BUSCAS FLEXÍVEIS (LIKE) ---

def buscar_clientes_pf_flexivel(termo):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes_pf WHERE nome LIKE ? OR cpf LIKE ?", (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def buscar_clientes_pj_flexivel(termo):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes_pj WHERE empresa LIKE ? OR fantasia LIKE ? OR cnpj LIKE ?", 
                   (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def buscar_produtos_flexivel(termo):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE produto LIKE ? OR fabricante LIKE ?", (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def buscar_servicos_flexivel(termo):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos WHERE descricao LIKE ?", (f"%{termo}%",))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def buscar_orcamentos_pendentes(termo=""):
    conn = conectar(); cursor = conn.cursor()
    query = "SELECT * FROM orcamentos WHERE status = 'Pendente' AND (nome_cliente LIKE ? OR documento LIKE ?)"
    cursor.execute(query, (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def buscar_itens_do_orcamento(id_orcamento):
    conn = conectar(); cursor = conn.cursor()
    query = """
        SELECT i.*, COALESCE(p.produto, s.descricao) as nome_item
        FROM orcamento_itens i
        LEFT JOIN produtos p ON i.referencia_id = p.id AND i.tipo_item = 'produto'
        LEFT JOIN servicos s ON i.referencia_id = s.id AND i.tipo_item = 'servico'
        WHERE i.id_orcamento = ? """
    cursor.execute(query, (id_orcamento,))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

# --- MÓDULO ORÇAMENTOS (SALVAMENTO) ---

def salvar_orcamento_completo(dados_h, lista_i):
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO orcamentos (tipo_cliente, cliente_id, nome_cliente, documento, endereco_completo, data_emissao, validade_dias, total_produtos, total_servicos, valor_geral, status) 
            VALUES (:tipo_cliente, :cliente_id, :nome_cliente, :documento, :endereco_completo, :data_emissao, :validade_dias, :total_produtos, :total_servicos, :valor_geral, :status)""", dados_h)
        id_orc = cursor.lastrowid
        for item in lista_i:
            cursor.execute("""INSERT INTO orcamento_itens (id_orcamento, referencia_id, tipo_item, quantidade, valor_unitario, valor_total_item) 
                VALUES (?, ?, ?, ?, ?, ?)""", (id_orc, item['id'], item['tipo'], item['qtd'], item['valor'], item['total']))
        conn.commit(); return True
    except Exception as e:
        print(f"Erro Orçamento: {e}"); conn.rollback(); return False
    finally: conn.close()

# --- MÓDULO O.S. (APROVAÇÃO E CONVERSÃO) ---

def aprovar_e_converter_orcamento(id_orcamento):
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM orcamentos WHERE id_orcamento = ?", (id_orcamento,))
        orc = cursor.fetchone()
        if not orc: return False
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute("""INSERT INTO ordens_servico (tipo_cliente, cliente_id, nome_cliente, documento, endereco_completo, data_emissao, data_aprovacao, total_produtos, total_servicos, valor_geral) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                       (orc['tipo_cliente'], orc['cliente_id'], orc['nome_cliente'], orc['documento'], 
                        orc['endereco_completo'], orc['data_emissao'], data_atual, orc['total_produtos'], orc['total_servicos'], orc['valor_geral']))
        id_nova_os = cursor.lastrowid
        cursor.execute("SELECT * FROM orcamento_itens WHERE id_orcamento = ?", (id_orcamento,))
        itens = cursor.fetchall()
        for item in itens:
            cursor.execute("""INSERT INTO os_itens (id_os, referencia_id, tipo_item, quantidade, valor_unitario, valor_total_item) 
                              VALUES (?, ?, ?, ?, ?, ?)""", (id_nova_os, item['referencia_id'], item['tipo_item'], item['quantidade'], item['valor_unitario'], item['valor_total_item']))
            if item['tipo_item'] == 'produto':
                cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (item['quantidade'], item['referencia_id']))
        cursor.execute("DELETE FROM orcamento_itens WHERE id_orcamento = ?",(id_orcamento,))
        cursor.execute("DELETE FROM orcamentos WHERE id_orcamento = ?",(id_orcamento,))
        conn.commit(); return True
    except Exception as e:
        print(f"Erro Conversão: {e}"); conn.rollback(); return False
    finally: conn.close()

def excluir_orcamento_recusado(id_orcamento):
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orcamento_itens WHERE id_orcamento = ?", (id_orcamento,))
        cursor.execute("DELETE FROM orcamentos WHERE id_orcamento = ?", (id_orcamento,))
        conn.commit(); return True
    except:
        conn.rollback(); return False
    finally: conn.close()
