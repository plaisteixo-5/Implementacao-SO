from typing import Type
from .ES import DriverES

class GerenciadorIO:


    def __init__(self) -> None:
        self.IOList = {}   
       
        

        #Fila de requisições para cada dispositivo, em seguida definiri a prioriadea

        
        #Rotina d etratamento de interrupção vetor de interrução ?!
        #pag 35 nos slides

    def inserirDispositivo(self, dispositivo: Type[DriverES]):
        #Mapear drive com o nome
        # gerarNome
        # inserir em IO List 

    def executarDispositivo(self, dispositivo: Type[DriverES]):
        self.IOList[dispositivo].executar()


    def gravarDadosEmRegistradores(self):
    def lerDadosDosRegistradores(self):
    