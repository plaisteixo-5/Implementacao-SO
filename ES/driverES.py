from abc import ABC, abstractclassmethod

class DriverES(ABC):
    #reentrantes, o que significa que um driver deve
    #supor que ele pode ser chamado uma segunda vez antes que a
        #primeira chamada tenha sido concluída.
    def __init__(self) -> None:
        self.memoria

    @abstractclassmethod
    def executar(self):
        pass

    @abstractclassmethod    
    def ler(self):
        pass

    @abstractclassmethod
    def escrever(self) -> None:
        pass

    @abstractclassmethod
    def interromper(self) -> None:
        pass