🛠️ Mundo do Autônomo
O Mundo do Autônomo é uma aplicação desktop de alta performance desenvolvida em Python para centralizar a gestão de profissionais autônomos e pequenos negócios. O sistema une uma interface moderna com uma lógica de negócio robusta, automatizando desde o orçamento até o fluxo de caixa.
🚀 Novas Funcionalidades e Progresso
✅ Gestão de Vendas e Serviços (Concluído)
Orçamentos Inteligentes: Adição de itens (produtos/serviços) com cálculo de totais em tempo real e geração de PDF profissional via FPDF.
Conversão para O.S.: Aprovação de orçamentos que gera automaticamente uma Ordem de Serviço, baixa o estoque e lança o valor no financeiro.
Controle de Estoque: Monitoramento automático de quantidades com sinalização visual de itens esgotados ou em nível crítico.
✅ Módulo Financeiro Integrado (Concluído)
Contas a Receber: Lançamentos automáticos vindos das O.S. e cadastros manuais, com sistema de "Baixa" e confirmação de forma de pagamento (Pix, Cartão, etc.).
Contas a Pagar: Gestão de despesas fixas e fornecedores com alertas de vencimento integrados.
Persistência Avançada: Relacionamento entre tabelas no SQLite3, garantindo integridade entre o que é vendido e o que é recebido.
🛠️ Tecnologias e Bibliotecas
Python 3.x: Linguagem core.
CustomTkinter: Interface gráfica ultra moderna com temas dinâmicos.
SQLite3: Banco de dados relacional embutido para persistência local.
FPDF: Biblioteca para geração dinâmica de documentos PDF.
Pillow (PIL): Processamento de imagens para logotipos e ícones.
📁 Estrutura do Projeto Atualizada
main.py: Ponto de entrada e inicialização do loop.
principal.py: Gerencia a janela raiz e componentes globais.
database.py: Core do sistema. Contém o esquema SQL e toda a lógica de persistência e automação (Conversão O.S -> Financeiro).
container.py: Cérebro da navegação e menu lateral.
orcamento.py: Módulo de vendas, carrinho de compras e geração de PDF.
os_modulo.py: Gestão de ordens de serviço pendentes e aprovadas.
cont_receber.py & cont_pagar.py: Módulos financeiros de controle de fluxo.
produtos.py & clientes.py: Telas de cadastro técnico e comercial.
🔧 Como Executar
Instale as dependências necessárias:
bash
pip install customtkinter pillow fpdf
Usa il codice con cautela.

Execute o sistema:
bash
python main.py
Usa il codice con cautela.

Nota: O banco de dados sistema_gestao.db é auto-gerado na primeira execução, criando todas as tabelas financeiras e operacionais necessárias.