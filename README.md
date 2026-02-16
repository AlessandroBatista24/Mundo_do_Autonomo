# Mundo do Autônomo 🛠️

O **Mundo do Autônomo** é uma aplicação desktop moderna desenvolvida em Python para centralizar a gestão de profissionais autônomos. O foco é oferecer agilidade no cadastro e controle financeiro através de uma interface intuitiva.

## 🚀 Progresso Atual e Funcionalidades

### ✅ Estrutura de Interface (Concluída)
- **Navegação Dinâmica:** Sistema de troca de telas otimizado que limpa a interface central e carrega novos módulos sem abrir novas janelas.
- **Identidade Visual Padronizada:** Design focado em usabilidade com widgets arredondados e paleta de cores verde/cinza customizada.
- **Arquitetura Modular:** Separação total de responsabilidades entre arquivos (Main, Principal, Containers e Negócio).

### ✅ Módulos Desenvolvidos
- **Cadastro de Pessoa Física:** Inclusão de CPF e dados de contato com sistema de limpeza automática de campos após salvar.
- **Cadastro de Pessoa Jurídica:** Estrutura pronta para CNPJ e Razão Social.
- **Gestão de Itens:** Módulos de Produtos e Serviços estruturados para futura integração com banco de dados.

## 🛠️ Tecnologias e Conceitos Aplicados

- **[Python 3.x](https://www.python.org):** Linguagem principal.
- **[CustomTkinter](https://customtkinter.tomschimansky.com):** Interface gráfica de alto nível com suporte a cantos arredondados (`corner_radius`).
- **Programação Orientada a Objetos (POO):** Uso intenso de herança (`CTkFrame`, `CTk`) para componentes reutilizáveis.
- **Dicionários Dinâmicos:** Armazenamento de referências de inputs para facilitar a integração com o [SQLite](https://docs.python.org).

## 📁 Organização dos Arquivos

- `main.py`: Inicializador do programa.
- `principal.py`: Maestro da janela principal e centralizador de containers.
- `container.py`: Lógica de navegação, menu lateral e cabeçalho.
- `clientes.py`: Telas de cadastro de Pessoa Física e Jurídica.
- `produtos.py`: Telas de cadastro de Produtos e Serviços.

## 🔧 Como Executar

1. **Instale as dependências:**
   ```bash
   pip install customtkinter
