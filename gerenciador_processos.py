from auxiliares import Receber_processos

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

        self.rt_processos = [x for x in self.todos_processos if x.prioridade == 0]
        self.user_processos = [x for x in self.todos_processos if x.prioridade != 0]

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
        print(f"##### Dispatcher #####")
        print(f'Processo ID: {processo.processo_ID}')
        print(f'Offset: {processo.offset}')
        print(f'Blocos: {processo.blocos_em_memoria}')
        print(f'Prioridade: {processo.prioridade}')
        print(f'Tempo: {processo.tempo_de_processador - processo.tempo_executado}')
        print(f'Impressora: {processo.requisicao_da_impressora}')
        print(f'Scanner: {processo.requisicao_do_scanner}')
        print(f'Modem: {processo.requisicao_do_modem}')
        print(f'Disco: {processo.requisicao_do_disco}')
        print()

    def run(self):
        processo_anterior = None
        processo_atual = None
        processos_terminados = 0

    