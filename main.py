from classes.Carro import Carro
from classes.Cidade import Cidade
from classes.Hora import Hora
from classes.Pedido import Pedido
from parsers import parser
from Simulador import Simulador
from queue import deque
import random

def gerar_frota(nr_eletricos, nr_combustao, locais):
     carros = {}
     for i in range(nr_combustao): # valores ajustados para o tipo
          autonomia = random.randint(350,500)
          cap = random.randint(1,7)
          custo = random.randint(3,7)
          impacto = random.randint(5,15)
          localizacao = locais[random.randint(0,len(locais)-1)]
          reabastecimento = random.randint(1,3)
          carros[i] = Carro(i,"Combustão",autonomia,cap,custo,impacto,localizacao,reabastecimento)
     
     for i in range(nr_combustao, nr_combustao+nr_eletricos):
          autonomia = random.randint(150,300)
          cap = random.randint(1,7)
          custo = random.randint(1,2)
          impacto = random.randint(0,2)
          localizacao = locais[random.randint(0,len(locais)-1)]
          reabastecimento = random.randint(5,8)
          carros[i] = Carro(i,"Elétrico",autonomia,cap,custo,impacto,localizacao,reabastecimento)
     
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
          if prioridade:
               tempo_espera = random.randint(5,10)
          else:
               tempo_espera = random.randint(15,30) # pedidos normais têm horário mais alargado

          pedidos.append(Pedido(origem,destino,passageiros,prioridade,round(random.random()) == 0,tempo_espera))
     
     return pedidos


def main():
     # podiamos gerar info aleatoria em vez de ler de um csv
     cidade = Cidade()
     carros = gerar_frota(10,10, cidade.getLocais()) # dps pedir como arg?
     pedidos = gerar_pedidos(500,cidade.getLocais())
     #carros, pedidos = parser( "data/Carros.csv", "data/Pedidos.csv")
     tempo = Hora(6,0)

     for algoritmo in range(1,5): # fazer simulação de todos os algoritmos?
          Simulador(carros.copy(),pedidos.copy(),tempo,cidade,algoritmo).run()

if __name__ == "__main__":
    main()