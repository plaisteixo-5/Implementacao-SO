from auxiliares import Receber_processos

lista_processos = Receber_processos('processos.txt')

for processo in lista_processos:
    tempo_de_inicialização = int(processo[0])
    prioridade = int(processo[1])
    tempo_de_processador = int(processo[2])
    blocos_em_memória = int(processo[3])
    numero_código_da_impressora_requisitada = int(processo[4])
    requisição_do_scanner = int(processo[5])
    requisição_do_modem = int(processo[6])
    número_código_do_disco = int(processo[7])

    