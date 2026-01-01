from classes.Cidade import Cidade
from classes.Hora import Hora
from Simulador import Simulador
from gerarDados import gerar_frota, gerar_pedidos
from parsers import parser

def main():
     cidade = Cidade()
     while True:
          print("Para esta simulação, pretende:")
          print("[1] Gerar novos dados aleatórios")
          print("[2] Usar veículo e pedidos previamente gerados")
          modo = int(input("\nA sua escolha é: "))
          if modo in range(1,3):
               break
          print("\nERRO: Escolha uma opção válida (1 ou 2)\n")

     if modo == 1:
          carros = gerar_frota(15,30) # veículos: 15 elétricos, 30 a combustão
          pedidos = gerar_pedidos(1000) # 1000 pedidos
     else:
          carros, pedidos = parser("data/Veiculos.csv", "data/Pedidos.csv")

     while True:
          print("Selecione o modo de simulação que pretende correr:")
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