import queue
MAX_PROCESSOS = 1000

# Fila de prioridade de tempo real
fila_prioridade_real = queue.PriorityQueue() # Usar FIFO

# Fila de prioridade de processos de usuario
fila_prioridade1_user = queue.PriorityQueue()
fila_prioridade2_user = queue.PriorityQueue()
fila_prioridade3_user = queue.PriorityQueue()


# Obter dados da file.txt
from auxiliares import Receber_files

lista_files = Receber_files('files.txt')

qtd_blocos = lista_files[0]
qtd_segmentos_ocupados = lista_files[1]
for operacao in lista_files[2]:
    id_processo = operacao[0]
    codigo_operacao = operacao[1]
    nome_arquivo = operacao[2]
    if len(operacao) > 3:
        numero_blocos = operacao[3]
        #esse só existe quando operaçoes é maior que 3.

