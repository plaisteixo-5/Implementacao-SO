from  .memoria import ListaDeBlocos

class GerenciadorMemoria:
    # lista encadeada de blocos livres
    # contiguas unir tudo em um espaço compacto
    # fazer tudo em função de listas pode ser melhro
    # B ou P - onde INicia - tamanho 
    def __init__(self) -> None:
        self.memoria = ListaDeBlocos();   

    def salvar(self, PID, tipo, tamanho):
        ListaDeBlocos.alocarMemoria(PID, tipo, tamanho)




