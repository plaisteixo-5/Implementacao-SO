from driverES import DriverES

class Modem(DriverES):
    def __init__(self) -> None:
        self.tipo = "MODEM"

    def executar(self):
        "Exencutando [MODEM]..."

    def interromper(self):
        print(" ---------------- Interrupção causada por [MODEM] ----------------")  