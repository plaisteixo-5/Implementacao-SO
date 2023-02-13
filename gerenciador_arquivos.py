class GerenciadorDeArquivos:
    def __init__(self, blocos_disco, segmento, arquivos):
        self.blocos_disco = 0
        self.segmento = 0
        self.arquivos = []
        self.memoria_auxiliar = []
        for _ in range(0, blocos_disco):
            self.memoria_auxiliar.append(' ')

        for arquivo in arquivos:
            posicao_inicial = int(arquivo[1])
            posicao_final = posicao_inicial + int(arquivo[2])

            for posicao_memoria in range(posicao_inicial, posicao_final):
                self.memoria_auxiliar[posicao_memoria] = arquivo[0]

    def SalvaArquivo(self, id_processo, nome_arquivo, quantidade_blocos):
        if(not self.ExisteArquivo(nome_arquivo)):
            tamanho_memoria = len(self.memoria_auxiliar)
            for index in range(0, tamanho_memoria):
                if self.memoria_auxiliar[index] == ' ':
                    sub_index = index + 1
                    contador = 1
                    while sub_index <= tamanho_memoria - 1 and self.memoria_auxiliar[sub_index] == ' ' and contador != quantidade_blocos and contador != int(quantidade_blocos):
                        contador += 1
                        sub_index += 1
                        
                    if contador == int(quantidade_blocos):
                        self.AlocaMemoria(nome_arquivo, index, int(quantidade_blocos))
                        self.PrintaMensagemDeSucessoArquivoSalvo(id_processo, nome_arquivo, index, sub_index)
                        return
                    
                    index = sub_index

            print(f'O processo {id_processo} não pode criar o arquivo {nome_arquivo} (falta de espaço).')
        else:
            print(f'Ja existe um arquivo com o nome {nome_arquivo}.')

    def AlocaMemoria(self, nome_arquivo, posicao_inicial, quantidade_blocos):
        blocos_restantes = quantidade_blocos
        endereco_inicial = posicao_inicial

        while blocos_restantes != 0:
            self.memoria_auxiliar[endereco_inicial] = nome_arquivo
            endereco_inicial += 1
            blocos_restantes -= 1
    
    def PrintaMensagemDeSucessoArquivoSalvo(self, id_processo, nome_arquivo, posicao_inicial, posicao_final):
        if(posicao_final-posicao_inicial == 1):
            print(f'O processo {id_processo} criou o arquivo {nome_arquivo} (bloco {posicao_inicial}).', end=" ")
        else:
            print(f'\nInicial:{posicao_inicial}\nfinal:{posicao_final}\n')
            for value in range(posicao_inicial, posicao_final):
                if value + 1 == posicao_final-1:
                    print(f'{value} e', end=" ")
                elif value == posicao_final-1:
                    print(f'{value}', end=" ")
                else:
                    print(f'{value},', end=" ")
            print(').')

    def DeletaArquivo(self, id_processo, nome_arquivo):
        if self.ExisteArquivo(nome_arquivo):
            for indice_memoria in range(0, len(self.memoria_auxiliar)):
                if self.memoria_auxiliar[indice_memoria] == nome_arquivo:
                    self.memoria_auxiliar[indice_memoria] = ' '
            
            print(f'O processo {id_processo} deletou o arquivo {nome_arquivo}')
        else:
            print(f'O processo {id_processo} não pode deletar o arquivo {nome_arquivo} porque ele não existe')
    
    def DesalocaMemoria(self, nome_arquivo):
        for memoria in self.memoria_auxiliar:
            if memoria == nome_arquivo:
                memoria = ' '

    
    def ExisteArquivo(self, nome_arquivo):
        if self.memoria_auxiliar.count(nome_arquivo):
            return True
        
        return False

    def PrintaMemoria(self):
        for memoria in self.memoria_auxiliar:
            if memoria == ' ':
                print('-', end=" ")
            else:
                print(f'{memoria}', end=" ")
        print("")