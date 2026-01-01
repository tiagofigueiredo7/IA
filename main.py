from classes.Cidade import Cidade
from classes.Hora import Hora
from Simulador import Simulador
from gerarDados import gerar_dados
from parsers import parser

def main():
     cidade = Cidade()
     while True:
          print("Para esta simulação, pretende:")
          print("[1] Gerar novos dados aleatórios")
          print("[2] Usar veículos e pedidos previamente gerados")
          modo = int(input("\nA sua escolha é: "))
          if modo in range(1,3):
               break
          print("\nERRO: Escolha uma opção válida (1 ou 2)\n")

     if modo == 1:
          carros, pedidos = gerar_dados(15,30,1000) # novos dados são criados e armazenados
     else:
          carros, pedidos = parser("data/Veiculos.csv", "data/Pedidos.csv") # dados lidos dos CSVs

     while True:
          print("\nSelecione o modo de simulação que pretende correr:")
          print("[1] Básico: É selecionado o primeiro carro disponível")
          print("[2] Rápido: É selecionado o carro que demore o mínimo a responder")
          print("[3] Económico: É selecionado o carro que custe o mínimo a fazer a viagem")
          print("[4] Ambiental: É selecionado o carro que liberte o mínimo de emissões durante a viagem")
          modo = int(input("\nA sua escolha é: "))
          if modo in range(1,5):
               break 
          print("\nERRO: Escolha uma opção válida (um número entre 1 e 4)\n")
     
     for algoritmo in range(4):
          Simulador(carros.copy(),pedidos.copy(),Hora(6,0),cidade,algoritmo+1,modo).run()

if __name__ == "__main__":
    main()