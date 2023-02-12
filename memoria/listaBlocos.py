from memoriaTipo import TipoMemoria
class Node:
    def __init__(self, id, tipo, tamanho):
        self.id = id
        self.tipo = tipo
        self.tamanho =tamanho
        self.next = None

class ListaDeBlocos:
    def __init__(self):
        self.head = Node("#NOID", TipoMemoria.TREAL_LIVRE, 64)
        self.head.next = Node("#NOID", TipoMemoria.PRCS_LIVRE, 960)
        self.exception = False

    
    def alocarMemoria(self, id, tipo, tamanho):
        new_node = Node(id, tipo, tamanho )
        node_atual = self.head
        
        total = 0
        while node_atual:
            if node_atual.tipo.value == new_node.tipo.value  -1 and node_atual.tamanho >= new_node.tamanho:
                if node_atual.tamanho - new_node.tamanho > 0:
                    node_intermediario = Node("#NOID", node_atual.tipo, node_atual.tamanho - new_node.tamanho)
                    node_intermediario.next = node_atual.next
                    node_atual.next = node_intermediario

                node_atual.id = new_node.id
                node_atual.tipo = TipoMemoria(node_atual.tipo.value + 1)
                node_atual.tamanho = new_node.tamanho
                return total
            
            elif total + node_atual.tamanho > 1024:
                if self.exception == False:
                    self.tratarInterrupcaoMemoria(new_node)
                return total
            total += node_atual.tamanho
            node_atual = node_atual.next


    def liberarMemoria(self, id):
        node_atual = self.head

        while node_atual:
            if node_atual.id == id:
                node_atual.tipo =  TipoMemoria(node_atual.tipo.value -1)
                node_atual.id = "#NOID"
                return
            node_atual = node_atual.next

        print("Não foi possível encontrar um processo com esse ID")

        return
        

    def lerProcessoNaMemoria( self, id):
        node_atual = self.head

        total  = 0
        while node_atual:
            if node_atual.id == id:
                print(total)
                print(node_atual.tamanho)
                print(node_atual.id)
                return
            total += node_atual.tamanho
            node_atual = node_atual.next

    def printEstadoMemoria(self):
        node_atual = self.head
        total = 0
        print(self.to_list())
        # while node_atual:
        #     print("Posição: ", total)
        #     print("Tamanho: ",node_atual.tamanho)
        #     print("Tipo: ",node_atual.tipo)
        #     print("ID: ",node_atual.id)
        #     print()
        #     total += node_atual.tamanho
        #     node_atual = node_atual.next

    def tratarInterrupcao(self, new_node):
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
        listaCompactada = sorted(arrayBlocos, key= lambda node: node[1].value, reverse = True)

        self.head = Node(listaCompactada[0][0], listaCompactada[0][1],  listaCompactada[0][2])
        listaCompactada.pop(0)
        
        node_atual = self.head
        idx  = 0
        for node in listaCompactada:
            idx+=1
            nodez = Node(node[0], node[1], node[2])
            node_atual.next = nodez
            node_atual = node_atual.next

        return

    def to_list(self):
        node_data = []
        current_node = self.head

        while current_node:
            node_data.append([current_node.id, current_node.tipo, current_node.tamanho])
            current_node = current_node.next

        return node_data

listaDeBlocos = ListaDeBlocos()
print(TipoMemoria.PRCS.value)
listaDeBlocos.alocarMemoria("PAA", TipoMemoria.PRCS, 50)
listaDeBlocos.alocarMemoria("JEA", TipoMemoria.PRCS, 80)
listaDeBlocos.alocarMemoria("DBP", TipoMemoria.PRCS, 120)
listaDeBlocos.alocarMemoria("SESF", TipoMemoria.PRCS, 400)
listaDeBlocos.printEstadoMemoria()
print("----------------")
listaDeBlocos.liberarMemoria("JEA")

listaDeBlocos.printEstadoMemoria()
print("----------------")


# listaDeBlocos.compactar()
listaDeBlocos.compactar()
listaDeBlocos.coealescer()
listaDeBlocos.printEstadoMemoria()
print("----------------")

