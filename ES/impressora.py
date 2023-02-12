from driverES import DriverES

class Impressora(DriverES):
    def __init__(self) -> None:
        self.tipo = "IMPRESSORA"

    def executar(self):
        "Exencutando [IMPRESSORA]..."

    def interromper(self):
        print(" ---------------- Interrupção causada por [IMPRESSORA] ----------------")
