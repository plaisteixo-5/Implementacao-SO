from gerenciador_processos import Processo, Gerenciador_de_processos
from gerenciador_arquivos import GerenciadorDeArquivos

class Kernel:
    def __init__(self):
        self.processos = []
        self.files = []
    
    def receber_processos(nome_arquivo:str) -> list:
        nome_arquivo = 'Arquivos/' + nome_arquivo   #Usado para a pasta
    
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            linhas = [x.strip() for x in linhas]
            lista = [x.split(', ') for x in linhas]
        return lista

    def receber_files(nome_arquivo:str) -> list:
        nome_arquivo = 'Arquivos/' + nome_arquivo   #Usado para a pasta

        with open(nome_arquivo, 'r') as arquivo:
            qtd_blocos = int(arquivo.readline().rstrip())
            n_segmentos_ocupados = int(arquivo.readline().rstrip())
            linhas = arquivo.readlines()
            linhas = [x.strip() for x in linhas]
            lista = [x.split(', ') for x in linhas]
            arquivos = lista[0:n_segmentos_ocupados]
            operacoes = lista[n_segmentos_ocupados:len(lista)]

            gerenciador_arquivos = GerenciadorDeArquivos(qtd_blocos, n_segmentos_ocupados, arquivos)

            for operacao in operacoes:
                if operacao[1] == '0':
                    gerenciador_arquivos.SalvaArquivo(id_processo=operacao[0], nome_arquivo=operacao[2], quantidade_blocos=operacao[3])
                else:
                    gerenciador_arquivos.DeletaArquivo(id_processo=operacao[0], nome_arquivo=operacao[2])

            gerenciador_arquivos.PrintaMemoria()

        return qtd_blocos, n_segmentos_ocupados, lista

    def run(self):
        nome_arquivo_processos = 'processos.txt'
        nome_arquivo_files = 'files.txt'

        lista_processos = Kernel.receber_processos(nome_arquivo_processos)

        qtd_processos = len(lista_processos)
        memoryOffSet = 0

        for i in range(qtd_processos):
            processo = lista_processos[i]

            if memoryOffSet == 0:
                Offset = 0
            else:
                Offset = memoryOffSet + 1

            self.processos.append(Processo(i, Offset, processo))
            memoryOffSet += int(processo[3])

        gerenciador_processos = Gerenciador_de_processos(self.processos)
        gerenciador_processos.run()


        # Aqui deve vir o código para o arquivo files.txt
    

    receber_files('files.txt')






