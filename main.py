from classes.Carro import Carro
from classes.Cidade import Cidade
from classes.Hora import Hora
from classes.Pedido import Pedido
from Simulador import Simulador
import random

def gerar_frota(nr_eletricos, nr_combustao, locais):
     carros = []
     for i in range(nr_eletricos):
          autonomia = random.randint(300,500)
          cap = random.randint(1,7)
          custo = random.randint(1,2)
          impacto = random.randint(0,1)
          localizacao = locais[random.randint(0,len(locais)-1)]
          reabastecimento = random.randint(10,25)
          carros.append(Carro(i,"Eletrico",autonomia,cap,custo,impacto,localizacao,reabastecimento))
     
     for i in range(nr_eletricos, nr_combustao+nr_eletricos): # valores ajustados para o tipo
          autonomia = random.randint(500,800)
          cap = random.randint(1,7)
          custo = random.randint(3,5)
          impacto = random.randint(5,15)
          localizacao = locais[random.randint(0,len(locais)-1)]
          reabastecimento = random.randint(1,2)
          carros.append(Carro(i,"Combustao",autonomia,cap,custo,impacto,localizacao,reabastecimento))
          
     return carros


def gerar_pedidos(nr_pedidos,locais):
     pedidos = []
     for _ in range(nr_pedidos):
          origem = locais[random.randint(0,len(locais)-1)]
          destino = locais[random.randint(0,len(locais)-1)]
          while destino == origem:
               destino = locais[random.randint(0,len(locais)-1)] # evitar pedidos estupidos
          passageiros = random.randint(1,5)
          prioridade = round(random.randint(1,5)) == 1 # 20% pedidos urgentes! 
          ambiental = round(random.randint(1,5)) == 1 # 20% pedidos vegans 
          if prioridade:
               tempo_espera = random.randint(5,15)
          else:
               tempo_espera = random.randint(15,30) # pedidos normais têm horário mais alargado

          pedidos.append(Pedido(origem,destino,passageiros,prioridade,ambiental,tempo_espera))
     
     return pedidos


def main():
     cidade = Cidade()
     carros = gerar_frota(15,30, cidade.getLocais())
     pedidos = gerar_pedidos(1000,cidade.getPontosColeta())

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
          cidade = Cidade()

if __name__ == "__main__":
    main()