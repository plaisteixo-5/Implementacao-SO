def Receber_processos(nome_arquivo:str) -> list:
    nome_arquivo = 'Arquivos/' + nome_arquivo   #Usado para a pasta
   
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        linhas = [x.strip() for x in linhas]
        lista = [x.split(', ') for x in linhas]
    return lista

def Receber_files(nome_arquivo:str) -> list:
    nome_arquivo = 'Arquivos/' + nome_arquivo   #Usado para a pasta
   
    with open(nome_arquivo, 'r') as arquivo:
        qtd_blocos = arquivo.readline().rstrip()
        n_segmentos_ocupados = arquivo.readline().rstrip()
        linhas = arquivo.readlines()
        linhas = [x.strip() for x in linhas]
        lista = [x.split(', ') for x in linhas]
    return qtd_blocos, n_segmentos_ocupados, lista

lista_processos = Receber_processos('processos.txt')
lista_files = Receber_files('files.txt')