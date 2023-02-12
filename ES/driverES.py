from abc import ABC, abstractclassmethod

class DriverES(ABC):
    #reentrantes, o que significa que um driver deve
    #supor que ele pode ser chamado uma segunda vez antes que a
        #primeira chamada tenha sido concluída.
    def __init__(self) -> None:
        self.tipo

    @abstractclassmethod
    def executar(self):
        pass

    @abstractclassmethod
    def interromper(self) -> None:
        pass