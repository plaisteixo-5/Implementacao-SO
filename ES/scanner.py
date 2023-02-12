from driverES import DriverES

class Scanner(DriverES):
    def __init__(self) -> None:
        self.tipo = "SCANNER"

    def executar(self):
        "Exencutando [Scanner]..."

    def interromper(self):
        print(" ---------------- Interrupção causada por [SCANNER] ----------------")