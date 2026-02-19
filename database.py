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
        
        # ... (Tabelas de Clientes, O.S., Orçamentos, Produtos e Serviços permanecem iguais)
        # Manter o que você já tem acima e ADICIONAR estas abaixo:

        # 1. TABELA CONTAS A RECEBER (ESSENCIAL PARA O LANÇAMENTO DA O.S.)
        cursor.execute("""CREATE TABLE IF NOT EXISTS contas_receber (
            id_receber INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL, 
            descricao TEXT NOT NULL, 
            id_os_origem INTEGER, 
            data_vencimento TEXT NOT NULL, 
            valor_total REAL NOT NULL,
            valor_recebido REAL DEFAULT 0, 
            data_recebimento TEXT, 
            forma_recebimento TEXT, 
            status TEXT DEFAULT 'PENDENTE')""")

        # 2. TABELA CONTAS A PAGAR
        cursor.execute("""CREATE TABLE IF NOT EXISTS contas_pagar (
            id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL, 
            credor TEXT NOT NULL, 
            data_vencimento TEXT NOT NULL,
            valor_original REAL NOT NULL, 
            valor_pago REAL DEFAULT 0,
            data_pagamento TEXT, 
            forma_pagamento TEXT, 
            status TEXT DEFAULT 'PENDENTE')""")

        # O restante (Estoque e Itens) continua igual
        cursor.execute("CREATE TABLE IF NOT EXISTS estoque (id_estoque INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER, qtd_atual REAL, qtd_minima REAL)")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS orcamento_itens (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT, id_orcamento INTEGER, 
            referencia_id INTEGER, tipo_item TEXT, quantidade REAL, 
            valor_unitario REAL, valor_total_item REAL)""")
        
        conn.commit()
        conn.close()
        print("Banco de dados e tabelas financeiras verificados com sucesso!")
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

def atualizar_cliente_pj(dados):
    """ Atualiza dados do cliente PJ baseado no CNPJ """
    conn = conectar(); cursor = conn.cursor()
    try:
        # O WHERE cnpj=:cnpj garante que alteramos a empresa certa
        cursor.execute("""UPDATE clientes_pj SET 
                          empresa=:empresa, fantasia=:fantasia, inscricao=:inscricao, 
                          logradouro=:logradouro, numero=:numero, bairro=:bairro, 
                          cidade=:cidade, estado=:estado, cep=:cep, 
                          telefone=:telefone, email=:email 
                          WHERE cnpj=:cnpj""", dados)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar PJ: {e}")
        return False
    finally:
        conn.close()


def deletar_cliente_pj(cnpj):
    """ Remove um cliente PJ pelo CNPJ """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes_pj WHERE cnpj = ?", (cnpj,))
        conn.commit(); return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar PJ: {e}"); return False
    finally: conn.close()


# --- MÓDULO PRODUTOS (CORRIGIDO) ---

def salvar_produto(dados):
    """ Insere um novo produto tratando os valores numéricos """
    conn = conectar(); cursor = conn.cursor()
    try:
        # Limpa R$, % e vírgulas antes de salvar
        d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
        
        cursor.execute("""INSERT INTO produtos (produto, fabricante, v_compra, imposto, custo_fixo, margem_lucro, quantidade, unidade, v_venda) 
            VALUES (:produto, :fabricante, :v_compra, :imposto, :custo_fixo, :margem_lucro, :quantidade, :unidade, :v_venda)""", d)
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar Produto: {e}")
        return False
    finally:
        conn.close()

def atualizar_produto_composto(dados, prod_original, fab_original):
    """ Atualiza o produto usando o nome e fabricante originais como referência """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_compra', 'v_venda', 'imposto', 'custo_fixo', 'margem_lucro', 'quantidade'])
        
        # Adicionamos os valores originais para o WHERE encontrar o item certo
        d['p_orig'] = prod_original
        d['f_orig'] = fab_original

        cursor.execute("""UPDATE produtos SET 
                          produto=:produto, fabricante=:fabricante, v_compra=:v_compra, 
                          imposto=:imposto, custo_fixo=:custo_fixo, margem_lucro=:margem_lucro, 
                          quantidade=:quantidade, unidade=:unidade, v_venda=:v_venda 
                          WHERE produto=:p_orig AND fabricante=:f_orig""", d)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar Produto: {e}")
        return False
    finally:
        conn.close()
def deletar_produto_composto(produto, fabricante):
    """ Remove um produto baseado no nome e fabricante """
    conn = conectar(); cursor = conn.cursor()
    try:
        # Primeiro, buscamos o ID para garantir a limpeza em orçamentos/os
        cursor.execute("SELECT id FROM produtos WHERE produto = ? AND fabricante = ?", (produto, fabricante))
        res = cursor.fetchone()
        
        if res:
            id_prod = res['id']
            # Limpeza preventiva para não dar erro de integridade
            cursor.execute("DELETE FROM orcamento_itens WHERE referencia_id = ? AND tipo_item = 'produto'", (id_prod,))
            cursor.execute("DELETE FROM os_itens WHERE referencia_id = ? AND tipo_item = 'produto'", (id_prod,))
            
            # Agora deleta o produto de fato
            cursor.execute("DELETE FROM produtos WHERE id = ?", (id_prod,))
            conn.commit()
            return True
        return False
    except Exception as e:
        print(f"Erro ao deletar Produto: {e}")
        return False
    finally:
        conn.close()


# --- MÓDULO SERVIÇOS (CORRIGIDO: SALVAR, ATUALIZAR E DELETAR) ---

def salvar_servico(dados):
    """ Insere um novo serviço tratando os valores numéricos """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
        cursor.execute("""INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final) 
            VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)""", d)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar Serviço: {e}"); return False
    finally: conn.close()

def atualizar_servico(dados, desc_original):
    """ Atualiza o serviço tratando valores e vinculando a descrição correta """
    conn = conectar(); cursor = conn.cursor()
    try:
        # 1. Limpa os valores (R$, vírgulas, etc)
        d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
        
        # 2. Garante que a descrição original está no dicionário para o WHERE
        d['desc_orig'] = desc_original
        
        # 3. Executa o SQL usando as chaves do dicionário (:chave)
        cursor.execute("""UPDATE servicos SET 
                          descricao=:descricao, 
                          v_custo=:v_custo, 
                          v_fixo=:v_fixo, 
                          v_imposto=:v_imposto, 
                          v_margem=:v_margem, 
                          v_final=:v_final 
                          WHERE descricao=:desc_orig""", d)
        
        conn.commit()
        return cursor.rowcount > 0 # Retorna True se uma linha foi alterada
    except Exception as e:
        print(f"Erro ao atualizar Serviço: {e}")
        return False
    finally: 
        conn.close()

def deletar_servico(descricao):
    """ Remove o serviço e limpa referências em orçamentos/OS para evitar erros """
    conn = conectar(); cursor = conn.cursor()
    try:
        # Busca o ID para limpar os itens vinculados antes de deletar o pai
        cursor.execute("SELECT id FROM servicos WHERE descricao = ?", (descricao,))
        res = cursor.fetchone()
        
        if res:
            id_serv = res['id']
            # Limpeza preventiva de vínculos
            cursor.execute("DELETE FROM orcamento_itens WHERE referencia_id = ? AND tipo_item = 'servico'", (id_serv,))
            cursor.execute("DELETE FROM os_itens WHERE referencia_id = ? AND tipo_item = 'servico'", (id_serv,))
            
            # Deleta o serviço
            cursor.execute("DELETE FROM servicos WHERE id = ?", (id_serv,))
            conn.commit(); return True
        return False
    except Exception as e:
        print(f"Erro ao deletar Serviço: {e}"); return False
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

# --- MÓDULO FINANCEIRO: CONTAS A PAGAR ---

def salvar_conta_pagar(dados):
    """ Insere uma nova conta pendente no banco de dados """
    conn = conectar(); cursor = conn.cursor()
    try:
        # Reutiliza sua função de tratamento para limpar R$ e vírgulas
        d = tratar_numericos(dados.copy(), ['valor_original'])
        cursor.execute("""INSERT INTO contas_pagar (descricao, credor, data_vencimento, valor_original) 
            VALUES (:descricao, :credor, :data_vencimento, :valor_original)""", d)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar Conta: {e}"); return False
    finally: conn.close()

def buscar_contas_pagar_flexivel(termo=""):
    """ Busca por credor ou descrição (seguindo seu padrão LIKE) """
    conn = conectar(); cursor = conn.cursor()
    query = """SELECT * FROM contas_pagar 
               WHERE (descricao LIKE ? OR credor LIKE ?)
               ORDER BY data_vencimento ASC"""
    cursor.execute(query, (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def baixar_conta_pagar(id_conta, dados_baixa):
    """ Registra o pagamento de uma conta (Baixa) """
    conn = conectar(); cursor = conn.cursor()
    try:
        # Criamos uma cópia para não alterar o dicionário original
        d = tratar_numericos(dados_baixa.copy(), ['valor_pago'])
        
        # ADICIONAMOS o id_conta dentro do dicionário 'd' para o SQL encontrar
        d['id_conta'] = id_conta 

        cursor.execute("""UPDATE contas_pagar SET 
                          valor_pago = :valor_pago, 
                          data_pagamento = :data_pagamento, 
                          forma_pagamento = :forma_pagamento, 
                          status = 'PAGO' 
                          WHERE id_conta = :id_conta""", d) # Agora usamos :id_conta aqui também
        
        conn.commit()
        return cursor.rowcount > 0 # Retorna True se realmente alterou a linha
    except Exception as e:
        print(f"Erro ao dar baixa: {e}")
        return False
    finally: 
        conn.close()



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
# =============================================================================
# MÓDULO SERVIÇOS (SALVAR, ATUALIZAR E DELETAR)
# =============================================================================

def salvar_servico(dados):
    """ Insere um novo serviço tratando os valores numéricos """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
        cursor.execute("""INSERT INTO servicos (descricao, v_custo, v_fixo, v_imposto, v_margem, v_final) 
            VALUES (:descricao, :v_custo, :v_fixo, :v_imposto, :v_margem, :v_final)""", d)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar Serviço: {e}"); return False
    finally: conn.close()

def atualizar_servico(dados, desc_original):
    """ Atualiza o serviço existente usando a descrição antiga como referência no WHERE """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['v_custo', 'v_fixo', 'v_imposto', 'v_margem', 'v_final'])
        d['desc_orig'] = desc_original
        cursor.execute("""UPDATE servicos SET 
                          descricao=:descricao, v_custo=:v_custo, v_fixo=:v_fixo, 
                          v_imposto=:v_imposto, v_margem=:v_margem, v_final=:v_final 
                          WHERE descricao=:desc_orig""", d)
        conn.commit(); return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar Serviço: {e}"); return False
    finally: conn.close()

def deletar_servico(descricao):
    """ Remove o serviço pelo nome """
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM servicos WHERE descricao = ?", (descricao,))
        conn.commit(); return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar Serviço: {e}"); return False
    finally: conn.close()


# =============================================================================
# MÓDULO O.S. (APROVAÇÃO, CONVERSÃO E FINANCEIRO AUTOMÁTICO)
# =============================================================================

def aprovar_e_converter_orcamento(id_orcamento):
    conn = conectar(); cursor = conn.cursor()
    try:
        # 1. Busca dados do orçamento original
        cursor.execute("SELECT * FROM orcamentos WHERE id_orcamento = ?", (id_orcamento,))
        orc = cursor.fetchone()
        if not orc: return False
        
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # 2. Insere na tabela de Ordens de Serviço (O.S.)
        cursor.execute("""INSERT INTO ordens_servico (tipo_cliente, cliente_id, nome_cliente, documento, endereco_completo, data_emissao, data_aprovacao, total_produtos, total_servicos, valor_geral) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                       (orc['tipo_cliente'], orc['cliente_id'], orc['nome_cliente'], orc['documento'], 
                        orc['endereco_completo'], orc['data_emissao'], data_atual, orc['total_produtos'], orc['total_servicos'], orc['valor_geral']))
        
        id_nova_os = cursor.lastrowid

        # 3. LANÇAMENTO NO FINANCEIRO (Onde estava o erro)
        # IMPORTANTE: Verifique se os nomes batem com sua tabela (cliente, descricao, id_os_origem, data_vencimento, valor_total, status)
        cursor.execute("""INSERT INTO contas_receber 
            (cliente, descricao, id_os_origem, data_vencimento, valor_total, status) 
            VALUES (?, ?, ?, ?, ?, 'PENDENTE')""", 
            (orc['nome_cliente'], f"Serviço O.S. Nº {id_nova_os}", id_nova_os, datetime.now().strftime("%d/%m/%Y"), orc['valor_geral']))

        # 4. Transfere os itens e baixa o estoque
        cursor.execute("SELECT * FROM orcamento_itens WHERE id_orcamento = ?", (id_orcamento,))
        itens = cursor.fetchall()
        for item in itens:
            cursor.execute("""INSERT INTO os_itens (id_os, referencia_id, tipo_item, quantidade, valor_unitario, valor_total_item) 
                              VALUES (?, ?, ?, ?, ?, ?)""", (id_nova_os, item['referencia_id'], item['tipo_item'], item['quantidade'], item['valor_unitario'], item['valor_total_item']))
            if item['tipo_item'] == 'produto':
                cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (item['quantidade'], item['referencia_id']))
        
        # 5. Remove orçamento antigo
        cursor.execute("DELETE FROM orcamento_itens WHERE id_orcamento = ?",(id_orcamento,))
        cursor.execute("DELETE FROM orcamentos WHERE id_orcamento = ?",(id_orcamento,))
        
        conn.commit()
        print(f"DEBUG: O.S {id_nova_os} e Lançamento Financeiro criados!") # Verifique se isso aparece no terminal
        return True
    except Exception as e:
        print(f"Erro na Conversão/Financeiro: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()



# =============================================================================
# MÓDULO CONTAS A RECEBER
# =============================================================================

def salvar_conta_receber(dados):
    """ Insere um novo título a receber manualmente """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados.copy(), ['valor_total'])
        cursor.execute("""INSERT INTO contas_receber 
            (cliente, descricao, data_vencimento, valor_total, status) 
            VALUES (:cliente, :descricao, :data_vencimento, :valor_total, 'PENDENTE')""", d)
        conn.commit(); return True
    except Exception as e:
        print(f"Erro ao salvar Conta a Receber: {e}"); return False
    finally: conn.close()

def buscar_contas_receber_flexivel(termo=""):
    """ Busca títulos por cliente ou descrição """
    conn = conectar(); cursor = conn.cursor()
    query = "SELECT * FROM contas_receber WHERE cliente LIKE ? OR descricao LIKE ? ORDER BY data_vencimento ASC"
    cursor.execute(query, (f"%{termo}%", f"%{termo}%"))
    res = [dict(l) for l in cursor.fetchall()]; conn.close(); return res

def baixar_conta_receber(id_receber, dados_baixa):
    """ Registra o recebimento e altera status para RECEBIDO """
    conn = conectar(); cursor = conn.cursor()
    try:
        d = tratar_numericos(dados_baixa.copy(), ['valor_recebido'])
        d['id_r'] = id_receber
        cursor.execute("""UPDATE contas_receber SET 
                          valor_recebido = :valor_recebido, data_recebimento = :data_recebimento, 
                          forma_recebimento = :forma_recebimento, status = 'RECEBIDO' 
                          WHERE id_receber = :id_r""", d)
        conn.commit(); return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao dar baixa no recebível: {e}"); return False
    finally: conn.close()
