# Importa a classe 'Criando_janela' do seu arquivo 'principal.py'
from principal import Criando_janela

# Verifica se este arquivo está sendo executado diretamente (e não importado por outro)
if __name__ == "__main__":
    
    # Instancia (cria na memória) o objeto da sua aplicação baseado na classe principal
    # Isso executa o método __init__ da sua janela e carrega todos os componentes
    app = Criando_janela()
    
    # Inicia o loop principal do Tkinter (Event Loop). 
    # Sem essa linha, a janela abriria e fecharia em milissegundos. 
    # Ela mantém o programa rodando e "ouvindo" cliques e comandos do usuário.
    app.mainloop()
