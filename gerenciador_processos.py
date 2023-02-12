class Processo:
    def __init__(self, pID, offset, processo):
        self.processo_ID = int(pID)
        self.tempo_de_inicialização = int(processo[0])
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

        self.todos_processos.sort(key=lambda x: x.tempo_de_inicialização)

        self.rt_processos = [x for x in self.todos_processos if int(x.prioridade) == 0]
        self.user_processos = [x for x in self.todos_processos if int(x.prioridade) != 0]

        print(f'Processos RT: {len(self.rt_processos)}')
        print(f'Processos User: {len(self.user_processos)}')
        print(f'Processos Todos: {len(self.todos_processos)}')


    def verificar_novo_processo(self):
        while self.rt_processos_auxID < len(self.rt_processos) and self.rt_processos[self.rt_processos_auxID].tempo_de_inicialização == self.tempo_atual:
            self.rt_processos_ready.append(self.rt_processos[self.rt_processos_auxID])
            self.rt_processos.sort(key=lambda x: x.prioridade)
            self.rt_processos_auxID += 1

        while self.user_processos_auxID < len(self.user_processos) and self.user_processos[self.user_processos_auxID].tempo_de_inicialização == self.tempo_atual:
            self.user_processos_ready.append(self.user_processos[self.user_processos_auxID])
            self.user_processos.sort(key=lambda x: x.prioridade)
            self.user_processos_auxID += 1

    def exibir_processos(self, processo):
        print(f"##### DESPACHANTE #####")
        print(f'\tProcesso ID: {processo.processo_ID}')
        print(f'\tOffset: {processo.offset}')
        print(f'\tBlocos: {processo.blocos_em_memoria}')
        print(f'\tPrioridade: {processo.prioridade}')
        print(f'\tTempo: {processo.tempo_de_processador - processo.tempo_executado}')
        print(f'\tImpressora: {processo.requisicao_da_impressora}')
        print(f'\tScanner: {processo.requisicao_do_scanner}')
        print(f'\tModem: {processo.requisicao_do_modem}')
        print(f'\tDisco: {processo.requisicao_do_disco}')
        print()

    def run(self):
        processo_anterior = -1
        processo_atual = -1
        processos_terminados = 0

        while processos_terminados < len(self.todos_processos):
            self.verificar_novo_processo()

            if processo_atual == -1:
                if len(self.rt_processos_ready) > 0: # Se houver processos RT
                    processo_atual = self.rt_processos_ready[0].processo_ID
                    self.rt_processos_ready.pop(0)
                    print(f'Processo RT {processo_atual} executando...')
                    if self.tabela_de_processos[processo_atual].executando() == False:
                        self.exibir_processos(self.tabela_de_processos[processo_atual])
                        
                    self.tabela_de_processos[processo_atual].tempo_executado += 1

                    if self.tabela_de_processos[processo_atual].terminado() == True:
                        processos_terminados += 1
                        processo_atual = -1
                        
                elif len(self.user_processos_ready) > 0: # Se não houver processos RT, mas houver processos USER
                    processo_atual = self.user_processos_ready[0].processo_ID
                    self.user_processos_ready.pop(0)

                    if self.tabela_de_processos[processo_atual].executando() == False:
                        self.exibir_processos(self.tabela_de_processos[processo_atual])

                    self.tabela_de_processos[processo_atual].tempo_executado += 1

                    if self.tabela_de_processos[processo_atual].terminado() == True:
                        processos_terminados += 1
                        processo_atual = -1

            else: # Se já houver um processo sendo executado
                if self.tabela_de_processos[processo_atual].prioridade == 0:
                    self.tabela_de_processos[processo_atual].tempo_executado += 1
                    if self.tabela_de_processos[processo_atual].terminado() == True:
                        processos_terminados += 1
                        processo_atual = -1
                    else:
                        processo_anterior = processo_atual
                else:
                    if(len(self.rt_processos_ready) > 0):
                        self.rt_processos_ready.append(self.tabela_de_processos[processo_atual])
                        self.rt_processos_ready.sort(key=lambda x: x.prioridade)

                        processo_atual = self.rt_processos_ready[0].processo_ID
                        self.rt_processos_ready.pop(0)
                        
                        if self.tabela_de_processos[processo_atual].executando() == False:
                            self.exibir_processos(self.tabela_de_processos[processo_atual])

                        self.tabela_de_processos[processo_atual].tempo_executado += 1

                        if self.tabela_de_processos[processo_atual].terminado() == True:
                            processos_terminados += 1
                            processo_atual = -1
                        else:   
                            processo_anterior = processo_atual
                    else:
                        if(len(self.user_processos_ready) > 0):
                            self.user_processos_ready.append(self.tabela_de_processos[processo_atual])
                            self.user_processos_ready.sort(key=lambda x: x.prioridade)

                            if self.tabela_de_processos[0].pID == processo_anterior and len(self.user_processos_ready) > 1:                            
                                processo_atual = self.user_processos_ready[1].processo_ID
                                self.user_processos_ready.pop(1)
                            else:
                                processo_atual = self.user_processos_ready[0].processo_ID
                                self.user_processos_ready.pop(0)


                            if self.tabela_de_processos[processo_atual].executando() == False:
                                self.exibir_processos(self.tabela_de_processos[processo_atual])

                            self.tabela_de_processos[processo_atual].tempo_executado += 1

                            if self.tabela_de_processos[processo_atual].terminado() == True:
                                processos_terminados += 1
                                processo_atual = -1
                            else:
                                processo_anterior = processo_atual
                        else:
                            self.tabela_de_processos[processo_atual].tempo_executado += 1
                            if self.tabela_de_processos[processo_atual].terminado() == True:
                                processos_terminados += 1
                                processo_atual = -1
                            else:
                                processo_anterior = processo_atual

            self.tempo_atual += 1
