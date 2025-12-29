from classes.Cidade import Cidade
from classes.Hora import Hora
from parsers import parser
from Simulador import Simulador

def main():
    carros, pedidos = parser( "data/Carros.csv", "data/Pedidos.csv")

    for algoritmo in range(4):
        Simulador(carros.copy(),pedidos.copy(),Hora(6,0),Cidade(),algoritmo+1,1).run()

if __name__ == "__main__":
    main()