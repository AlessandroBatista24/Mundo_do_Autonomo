Mundo do Autônomo 🛠️
O Mundo do Autônomo é uma aplicação desktop moderna desenvolvida em Python para centralizar a gestão de profissionais autônomos. O foco é oferecer agilidade no cadastro e controle financeiro através de uma interface intuitiva e persistência de dados robusta.
🚀 Progresso Atual e Funcionalidades
✅ Estrutura de Interface (Concluída)
Navegação Dinâmica: Sistema de troca de telas otimizado que limpa a interface central e carrega novos módulos sem abrir novas janelas.
Identidade Visual Padronizada: Design focado em usabilidade com widgets arredondados e paleta de cores verde/cinza customizada.
Arquitetura Modular: Separação total de responsabilidades entre arquivos (Main, Principal, Containers e Negócio).
✅ Módulos Desenvolvidos
Cadastro de Clientes (PF/PJ): Inclusão de CPF/CNPJ e dados de contato com persistência direta no banco de dados.
Gestão de Produtos: Cadastro completo com sistema de cálculo em tempo real de preço de venda (Custo + Impostos + Margem %).
Gestão de Serviços: Módulo dedicado para precificação de mão de obra com cálculo automatizado.
Persistência de Dados: Integração total com SQLite para armazenamento permanente.
🛠️ Tecnologias e Conceitos Aplicados
Python 3.x: Linguagem principal.
CustomTkinter: Interface gráfica moderna com suporte a temas e cantos arredondados.
SQLite3: Banco de dados relacional embutido (sem necessidade de instalação externa).
POO (Programação Orientada a Objetos): Uso de herança e composição para criar componentes reutilizáveis.
Lógica de Eventos: Uso de bind("<KeyRelease>") para feedback visual e cálculos instantâneos na interface.
📁 Organização dos Arquivos
main.py: Inicializador do programa e loop principal.
principal.py: Maestro da janela e responsável por disparar a criação do banco de dados.
database.py: Core do sistema. Contém a estrutura das tabelas (SQL) e as funções de inserção e tratamento de dados.
container.py: Cérebro da navegação, gerenciando o menu lateral e a troca de frames.
clientes.py: Lógica das telas de Pessoa Física e Jurídica.
produtos.py: Lógica de precificação, widgets dinâmicos (ComboBox) e cadastro de itens/serviços
🔧 Como Executar
Instale as dependências:
bash
pip install customtkinter
Usa il codice con cautela.

Execute o sistema:
bash
python main.py
Usa il codice con cautela.

Nota: O banco de dados sistema_gestao.db será criado automaticamente na primeira execução.