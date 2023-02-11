from memoriaTipo import TipoMemoria
class Node:
    def __init__(self, id, tipo, tamanho):
        self.id = id
        self.tipo = tipo
        self.tamanho =tamanho
        self.next = None

class ListaDeBlocos:
    def __init__(self):
        self.head = Node(None, TipoMemoria.TREAL_LIVRE, 64)
        self.head.next = Node(None, TipoMemoria.PRCS_LIVRE, 960)
        self.exception = False
    
    def alocarMemoria(self, id, tipo, tamanho):
        new_node = Node(id, tipo, tamanho )
        node_atual = self.head

        total = 0
        while node_atual.next:
            if node_atual.tipo == new_node.tipo-1 and node_atual.tamanho >= new_node.tamanho:
                if node_atual.tamanho - new_node.tamanho > 0:
                    node_intermediario = Node(None, node_atual.tipo, node_atual.tamanho - new_node.tamanho)
                    node_intermediario.next = node_atual.next
                    node_atual.next = node_intermediario

                node_atual.id = new_node.id
                node_atual.tipo += 1
                node_atual.tamanho = new_node.tamanho
                return
            
            elif total + node_atual.tamanho > 1024:
                if self.exception == False:
                    self.tratarInterrupcaoMemoria(new_node)
                return
            node_atual = node_atual.next

    def liberarMemoria(self, id):
        node_atual = self.head

        while node_atual.next:
            if node_atual.id == id:
                node_atual.tipo -= 1
                node_atual.id = None
                return
            node_atual = node_atual.next

        print("Não foi possível encontrar um processo com esse ID")

        return


    def tratarInterrupcaoMemoria(self, new_node):
        self.compactar()
        self.coalescer()
        self.exception = True
        self.alocarMemoria(new_node.id, new_node.tipo, new_node.tamanho)
        self.exception = False

    def coealescer(self):

        node_atual = self.head

        while node_atual.next:
            if(node_atual.tipo == TipoMemoria.PRCS_LIVRE or node_atual.tipo == TipoMemoria.TREAL_LIVRE) and node_atual.tipo == node_atual.next.tipo:
                node_atual.tamanho += node_atual.next.tamanho
                node_atual.next = node_atual.next.next
                node_atual = node_atual
            else:
                node_atual = node_atual.next

        return

    def compactar(self):
        arrayBlocos = self.to_list()
        listaCompactada = sorted(arrayBlocos, key= lambda node: node.tipo, reverse = True)

        self.head = Node(listaCompactada[0][1], listaCompactada[0][0], listaCompactada[0][2])
        listaCompactada.pop(0)

        node_atual = self.head
        for node in listaCompactada:
            node_atual.next = Node(node[0][1], node[0][0], node[0][2])
            node_atual = node_atual.next

        return

    def to_list(self):
        node_data = []
        current_node = self.head

        while current_node.next:
            node_data.append({current_node.id, current_node.tipo, current_node.tamanho})
            current_node = current_node.next

        return node_data



