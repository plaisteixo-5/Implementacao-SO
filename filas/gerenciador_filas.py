import queue
import time
MAX_PROCESSOS = 1000
MAX_WAIT_TIME = 5

class Processo:
    def __init__(self, prioridade, id, tempo):
        self.prioridade = prioridade
        self.id = id
        self.tempo = tempo


class filas:
    def __init__(self):
        self.qtd_processos = 0
        self.filas_prioridade = [
            queue.Queue(),  # index 0  - Fila tempo real
            queue.Queue(),  # index 1  - Fila usuario 1
            queue.Queue(),  # index 2  - Fila usuario 2
            queue.Queue(),  # index 3  - Fila usuario 3
        ]

    def next(self):
        self.qtd_processos -= 1
        processo  = self.montarProcessosProntos().get()
        for i in list(self.montarProcessosProntos().queue): print(i.id)

        processo.tempo -= 1
        time.sleep(0.001)
        if processo.tempo > 0:
            if processo.prioridade > 0 and processo.prioridade < 3:
                processo.prioridade +=1
            self.enfileirar(processo, processo.prioridade)
        return processo

    def montarProcessosProntos(self):
        processosProntos =  queue.Queue(MAX_PROCESSOS)
        q0 = list(self.filas_prioridade[0].queue)
        q1 = list(self.filas_prioridade[1].queue)
        q2 = list(self.filas_prioridade[2].queue)
        q3 = list(self.filas_prioridade[3].queue)
        for i in q0: processosProntos.put(i)
        for i in q1: processosProntos.put(i)
        for i in q2: processosProntos.put(i)
        for i in q3: processosProntos.put(i)
        return processosProntos

    def estadoFilas(self):
        q0 = list(self.filas_prioridade[0].queue)
        q1 = list(self.filas_prioridade[1].queue)
        q2 = list(self.filas_prioridade[2].queue)
        q3 = list(self.filas_prioridade[3].queue)
        for i in q0:
            print("0: ", i.id) 
        for i in q1:
            print("1: ", i.id) 
        for i in q2: 
            print("2: ", i.id) 
        for i in q3: 
            print("3: ", i.id) 
    
    
    def enfileirar(self, elem, prioridade):
        if self.qtd_processos <= MAX_PROCESSOS:
            self.qtd_processos+=1
            self.filas_prioridade[prioridade].put(elem)

    def aging(self):
        for priority in range(1,4):
            for i in self.filas_prioridade[priority].queue:
                process = self.filas_prioridade[priority].get()
                if not process.waitTime:
                    process.waitTime = 1
                else:
                    process.waitTime +=1
                if(process.waitTime >= MAX_WAIT_TIME and process.prioridade > 1):
                    process.prioridade -= 1
                self.enfileirar(process, process.prioridade)

gF = filas()
p1 = Processo(1, "1", 2)
p2 = Processo(2, "2", 3)
p3 = Processo(3, "3", 1)
p4 = Processo(1, "4", 6)
p5 = Processo(1, "5", 3)
gF.enfileirar(p1, p1.prioridade)
gF.enfileirar(p2, p2.prioridade)
gF.enfileirar(p3, p3.prioridade)
gF.enfileirar(p4, p4.prioridade)
gF.enfileirar(p5, p5.prioridade)
gF.estadoFilas()
proc = gF.next()


                


        
        

    





    

