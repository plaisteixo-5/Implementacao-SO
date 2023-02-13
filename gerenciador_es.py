from typing import Type
from ES import DriverES
from ES import Syscalls
from ES import Impressora

class GerenciadorIO:
    def __init__(self) -> None:
        self.IOList = {} 
        self.qtdDispositivos = 0
        self.dispositivos = {
                            'scanner':[1,[]],
                            'impressora':[2,[]],
                            'modem':[1,[]],                    
                            'sata':[2,[]]}
       
    def inserirDispositivo(self, dispositivo: Type[DriverES]):
        self.IOList["#"+self.qtdDispositivos+dispositivo.tipo] = dispositivo
        # gerenciadorMemoria.
        
    def sysCall(self, id, syscall):
        if(syscall == Syscalls.EXECUTAR):
            self.IOList[id].executar()
        elif(syscall == Syscalls.INTERROMPER):
            self.IOList[id].interromper()

    def removerDispositivo(self, id):
        self.IOList.pop(id)

GIO  = GerenciadorIO()
GIO.inserirDispositivo(Impressora())