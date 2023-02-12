class Processo:
    def __init__(self, pID, offset, processo):
        self.processo_ID = int(pID)
        self.tempo_de_inicializacao = int(processo[0])
        self.prioridade = int(processo[1])
        self.tempo_de_processador = int(processo[2])
        self.blocos_em_memoria = int(processo[3])
        self.requisicao_da_impressora = int(processo[4])
        self.requisicao_do_scanner = int(processo[5])
        self.requisicao_do_modem = int(processo[6])
        self.requisicao_do_disco = int(processo[7])
        self.offset = int(offset)
        self.tempo_executado = 0

    def executando(self):
        if self.tempo_executado > 0:
            return True
        else:
            return False
    
    def terminado(self):
        if self.tempo_executado == self.tempo_de_processador:
            return True
        else:
            return False

class Gerenciador_de_processos:
    def __init__(self, processos):
        self.todos_processos = []
        self.rt_processos = []
        self.user_processos = []
        self.rt_processos_ready = []
        self.user_processos_ready = []
        self.rt_processos_auxID = 0
        self.user_processos_auxID = 0
        self.tempo_atual = 0
        self.tabela_de_processos = {}

        for processo in processos:
            self.todos_processos.append(processo)

        self.todos_processos.sort(key=lambda x: x.tempo_de_inicializacao)

        self.tabela_de_processos = {x.processo_ID: x for x in self.todos_processos}
        self.rt_processos = [x for x in self.todos_processos if int(x.prioridade) == 0]
        self.user_processos = [x for x in self.todos_processos if int(x.prioridade) != 0]

    def verificar_novo_processo(self):
        while self.rt_processos_auxID < len(self.rt_processos) and self.rt_processos[self.rt_processos_auxID].tempo_de_inicializacao == self.tempo_atual:
            self.rt_processos_ready.append(self.rt_processos[self.rt_processos_auxID])
            self.rt_processos_ready.sort(key=lambda x: x.prioridade)
            self.rt_processos_auxID += 1

        while self.user_processos_auxID < len(self.user_processos) and self.user_processos[self.user_processos_auxID].tempo_de_inicializacao == self.tempo_atual:
            self.user_processos_ready.append(self.user_processos[self.user_processos_auxID])
            self.user_processos_ready.sort(key=lambda x: x.prioridade)
            self.user_processos_auxID += 1

    def exibir_processos(self, processo):
        print(f"dispatcher =>")
        print(f'  PID: {processo.processo_ID}')
        print(f'  offset: {processo.offset}')
        print(f'  blocks: {processo.blocos_em_memoria}')
        print(f'  priority: {processo.prioridade}')
        print(f'  time: {processo.tempo_de_processador}')
        print(f'  printers: {processo.requisicao_da_impressora}')
        print(f'  scanners: {processo.requisicao_do_scanner}')
        print(f'  modems: {processo.requisicao_do_modem}')
        print(f'  drives: {processo.requisicao_do_disco}')
        print()

    def run(self):

        processo_anterior = None
        processo_atual = None
        processos_terminados = 0

        while processos_terminados < len(self.todos_processos):

            self.verificar_novo_processo()
            
            if processo_atual == None:
                if len(self.rt_processos_ready) > 0:
                    processo_atual = self.rt_processos_ready[0].processo_ID
                    self.rt_processos_ready.pop(0)

                    if self.tabela_de_processos[processo_atual].executando() == False:
                        self.exibir_processos(self.tabela_de_processos[processo_atual])

                    print(f'process {processo_atual} =>')
                    print(f'P{processo_atual} STARTED')
                    print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')

                    self.tabela_de_processos[processo_atual].tempo_executado += 1

                    if self.tabela_de_processos[processo_atual].terminado() == True:
                        print(f'P{processo_atual} return SIGINT\n')
                        processos_terminados += 1
                        processo_atual = None
                    else:
                        processo_anterior = processo_atual
                else:
                    if len(self.user_processos_ready) > 0:
                        processo_atual = self.user_processos_ready[0].processo_ID
                        self.user_processos_ready.pop(0)

                        if self.tabela_de_processos[processo_atual].executando() == False:
                            self.exibir_processos(self.tabela_de_processos[processo_atual])

                        print(f'process {processo_atual} =>')
                        print(f'P{processo_atual} STARTED')
                        print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')
                        
                        self.tabela_de_processos[processo_atual].tempo_executado += 1
                        
                        if self.tabela_de_processos[processo_atual].terminado() == True:
                            print(f'P{processo_atual} return SIGINT\n')
                            processos_terminados += 1
                            processo_atual = None
                        else:
                            processo_anterior = processo_atual

            else:
                if self.tabela_de_processos[processo_atual].prioridade == 0:
                    self.tabela_de_processos[processo_atual].tempo_executado += 1
                    print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')

                    if self.tabela_de_processos[processo_atual].terminado() == True:
                        processos_terminados += 1
                        print(f'P{processo_atual} return SIGINT\n')
                        processo_atual = None
                    else:
                        processo_anterior = processo_atual
                else:
                    if(len(self.rt_processos_ready) > 0):
                        print(f'P{processo_atual} STOPPED\n')

                        self.user_processos_ready.append(self.tabela_de_processos[processo_atual])
                        self.user_processos_ready.sort(key=lambda x: x.prioridade)

                        processo_atual = self.rt_processos_ready[0].processo_ID
                        self.rt_processos_ready.pop(0)

                        if self.tabela_de_processos[processo_atual].executando() == False:
                            self.exibir_processos(self.tabela_de_processos[processo_atual])

                        print(f'process {processo_atual} =>')
                        print(f'P{processo_atual} STARTED')
                        print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')
                        
                        self.tabela_de_processos[processo_atual].tempo_executado += 1
                        
                        if self.tabela_de_processos[processo_atual].terminado() == True:
                            processos_terminados += 1
                            print(f'P{processo_atual} return SIGINT\n')
                            processo_atual = None
                        else:
                            processo_anterior = processo_atual
                    else:
                        if(len(self.user_processos_ready) > 0):
                            print(f'P{processo_atual} STOPPED\n')

                            self.user_processos_ready.append(self.tabela_de_processos[processo_atual])
                            self.user_processos_ready.sort(key=lambda x: x.prioridade)

                            if self.user_processos_ready[0].processo_ID == processo_anterior and len(self.user_processos_ready) > 1:
                                processo_atual = self.user_processos_ready[1].processo_ID
                                self.user_processos_ready.pop(1)
                            else:
                                processo_atual = self.user_processos_ready[0].processo_ID
                                self.user_processos_ready.pop(0)
                            
                            if self.tabela_de_processos[processo_atual].executando() == False:
                                self.exibir_processos(self.tabela_de_processos[processo_atual])

                            print(f'process {processo_atual} =>')
                            print(f'P{processo_atual} STARTED')
                            print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')

                            self.tabela_de_processos[processo_atual].tempo_executado += 1

                            if self.tabela_de_processos[processo_atual].terminado() == True:
                                processos_terminados += 1
                                print(f'P{processo_atual} return SIGINT\n')
                                processo_atual = None
                            else:
                                processo_anterior = processo_atual
                        else:
                            print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')
                            self.tabela_de_processos[processo_atual].tempo_executado += 1
                            
                            if self.tabela_de_processos[processo_atual].terminado() == True:
                                processos_terminados += 1
                                print(f'P{processo_atual} return SIGINT\n')
                                processo_atual = None
                            else:
                                processo_anterior = processo_atual

            self.tempo_atual += 1