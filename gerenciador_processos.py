from time import sleep
from listaBlocos import ListaDeBlocos
from memoriaTipo import TipoMemoria

N_CICLOS = 5
TEMPO_SLEEP_CURTO = 0.4
TEMPO_SLEEP_LONGO = 0.8

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
        self.ciclos = N_CICLOS
        self.tabela_de_processos = {}
        self.memoria = ListaDeBlocos()

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
        sleep(TEMPO_SLEEP_LONGO)

    def run(self):
        processo_anterior = None
        processo_atual = None
        processos_terminados = 0

        while processos_terminados < len(self.todos_processos):
            sleep(0.05)
            self.verificar_novo_processo()
            
            if processo_atual == None: # se não houver processo atual
                if len(self.rt_processos_ready) > 0: # se houver processos RT
                    processo_atual = self.rt_processos_ready[0].processo_ID # pega o id do primeiro processo RT
                    self.rt_processos_ready.pop(0) # remove o processo RT da lista de processos RT prontos

                    if self.tabela_de_processos[processo_atual].executando() == False: # se o processo não estiver executando
                        self.exibir_processos(self.tabela_de_processos[processo_atual]) # exibe as informações do processo
                        # alocar memória
                        self.memoria.alocarMemoria(self.tabela_de_processos[processo_atual].processo_ID, TipoMemoria.TREAL, self.tabela_de_processos[processo_atual].blocos_em_memoria)

                    print(f'process {processo_atual} =>')
                    print(f'P{processo_atual} STARTED')
                    print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')

                    self.tabela_de_processos[processo_atual].tempo_executado += 1

                    if self.tabela_de_processos[processo_atual].terminado() == True: # se o processo terminou
                        #liberar memoria
                        self.memoria.liberarMemoria(self.tabela_de_processos[processo_atual].processo_ID)
                        print(f'P{processo_atual} return SIGINT\n') 
                        processos_terminados += 1
                        processo_atual = None # processo atual é nulo
                    else:
                        processo_anterior = processo_atual # se não terminou, o processo anterior é o processo atual
                else: # se não houver processos RT e houver processos USER
                    if len(self.user_processos_ready) > 0:
                        processo_atual = self.user_processos_ready[0].processo_ID
                        self.user_processos_ready.pop(0)

                        if self.tabela_de_processos[processo_atual].executando() == False:
                            self.exibir_processos(self.tabela_de_processos[processo_atual])
                            # alocar memória
                            self.memoria.alocarMemoria(self.tabela_de_processos[processo_atual].processo_ID, TipoMemoria.PRCS, self.tabela_de_processos[processo_atual].blocos_em_memoria)

                        print(f'process {processo_atual} =>')
                        print(f'P{processo_atual} STARTED')
                        print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')
                        

                        self.tabela_de_processos[processo_atual].tempo_executado += 1
                        
                        if self.tabela_de_processos[processo_atual].terminado() == True:
                            #liberar memoria
                            self.memoria.liberarMemoria(self.tabela_de_processos[processo_atual].processo_ID)
                            print(f'P{processo_atual} return SIGINT\n')
                            processos_terminados += 1
                            processo_atual = None
                        else:
                            processo_anterior = processo_atual

            else: # se houver processo atual
                if self.tabela_de_processos[processo_atual].prioridade == 0: # verifica se o processo atual é RT
                    self.tabela_de_processos[processo_atual].tempo_executado += 1
                    print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')

                    if self.tabela_de_processos[processo_atual].terminado() == True:
                        #liberar memoria
                        self.memoria.liberarMemoria(self.tabela_de_processos[processo_atual].processo_ID)
                        print(f'P{processo_atual} return SIGINT\n')
                        processos_terminados += 1
                        processo_atual = None
                    else:
                        processo_anterior = processo_atual
                else: # verifica se o processo atual é USER
                    if(len(self.rt_processos_ready) > 0): # verifica se existe um processo RT pronto
                        print(f'P{processo_atual} STOPPED\n')

                        self.user_processos_ready.append(self.tabela_de_processos[processo_atual]) # devolve o processo atual para a lista de processos USER prontos
                        self.user_processos_ready.sort(key=lambda x: x.prioridade) # ordena a lista de processos USER prontos

                        processo_atual = self.rt_processos_ready[0].processo_ID # pega o id do primeiro processo RT
                        self.rt_processos_ready.pop(0) # remove o processo RT da lista de processos RT prontos
                        sleep(TEMPO_SLEEP_CURTO)
                        if self.tabela_de_processos[processo_atual].executando() == False:
                            self.exibir_processos(self.tabela_de_processos[processo_atual])
                            # alocar memória
                            self.memoria.alocarMemoria(self.tabela_de_processos[processo_atual].processo_ID, TipoMemoria.TREAL, self.tabela_de_processos[processo_atual].blocos_em_memoria)

                        print(f'process {processo_atual} =>')
                        print(f'P{processo_atual} STARTED')
                        print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')
                        
                        self.tabela_de_processos[processo_atual].tempo_executado += 1
                        
                        if self.tabela_de_processos[processo_atual].terminado() == True:
                            #liberar memoria
                            self.memoria.liberarMemoria(self.tabela_de_processos[processo_atual].processo_ID)
                            print(f'P{processo_atual} return SIGINT\n')
                            processos_terminados += 1
                            processo_atual = None
                        else:
                            processo_anterior = processo_atual
                    else: # se não houver processos RT, logo USER
                        if(len(self.user_processos_ready) > 0): # verifica se existe pelo outro processo USER pronto
                            #Aqui pode ter uma realimentação de processos USER
                           
                            #verificar se o proximo tem prioridade maior que o atual
                            if (self.user_processos_ready[0].prioridade < self.tabela_de_processos[processo_atual].prioridade and self.ciclos <= 0) or self.ciclos <= 0:
                                print(f'P{processo_atual} STOPPED\n')
                                self.tabela_de_processos[processo_atual].prioridade += 1
                                self.user_processos_ready.append(self.tabela_de_processos[processo_atual]) # devolve o processo atual para a lista de processos USER prontos
                                processo_atual = self.user_processos_ready[0].processo_ID # pega o id do primeiro processo USER
                                self.user_processos_ready.pop(0)
                                self.user_processos_ready.sort(key=lambda x: x.prioridade) # ordena a lista de processos USER prontos
                                self.ciclos = N_CICLOS
                                print(f'process {processo_atual} =>')
                                print(f'P{processo_atual} STARTED')
                                sleep(TEMPO_SLEEP_CURTO)
                        
                            self.ciclos -= 1
                                                    
                            if self.tabela_de_processos[processo_atual].executando() == False:
                                self.exibir_processos(self.tabela_de_processos[processo_atual])
                                # alocar memória
                                self.memoria.alocarMemoria(self.tabela_de_processos[processo_atual].processo_ID, TipoMemoria.PRCS, self.tabela_de_processos[processo_atual].blocos_em_memoria)

                            print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')

                            self.tabela_de_processos[processo_atual].tempo_executado += 1

                            if self.tabela_de_processos[processo_atual].terminado() == True:
                                processos_terminados += 1
                                #liberar memoria
                                self.memoria.liberarMemoria(self.tabela_de_processos[processo_atual].processo_ID)
                                print(f'P{processo_atual} return SIGINT\n')
                                processo_atual = None
                                self.ciclos = N_CICLOS
                            else:
                                processo_anterior = processo_atual
                            
                        else:
                            print(f'P{processo_atual} instructions {self.tabela_de_processos[processo_atual].tempo_executado + 1}')
                            self.tabela_de_processos[processo_atual].tempo_executado += 1
                            
                            if self.tabela_de_processos[processo_atual].terminado() == True:
                                #liberar memoria
                                self.memoria.liberarMemoria(self.tabela_de_processos[processo_atual].processo_ID)
                                print(f'P{processo_atual} return SIGINT\n')
                                processos_terminados += 1
                                processo_atual = None
                            else:
                                processo_anterior = processo_atual

            self.tempo_atual += 1