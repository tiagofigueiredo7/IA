import csv
from classes.Carro import Carro
from classes.Pedido import Pedido
import random

pontos_coleta = ["Arcozelo","Barcelos","Rio Covo","Barcelinhos","Vila Boa","Silva","Lijó","Vila Frescainha","Várzea","Aguiar","Balugães","Chorente","Alvito","Panque"]

def gerar_frota(nr_eletricos, nr_combustao):
     carros = []
     for i in range(nr_eletricos):
          autonomia = random.randint(300,500)
          cap = random.randint(1,7)
          custo = random.randint(1,2)
          impacto = random.randint(0,1)
          localizacao = pontos_coleta[random.randint(0,len(pontos_coleta)-1)]
          reabastecimento = random.randint(10,25)
          carros.append(Carro(i,"Eletrico",autonomia,cap,custo,impacto,localizacao,reabastecimento))
     
     for i in range(nr_eletricos, nr_combustao+nr_eletricos): # valores ajustados para o tipo
          autonomia = random.randint(500,800)
          cap = random.randint(1,7)
          custo = random.randint(3,5)
          impacto = random.randint(5,15)
          localizacao = pontos_coleta[random.randint(0,len(pontos_coleta)-1)]
          reabastecimento = random.randint(1,2)
          carros.append(Carro(i,"Combustao",autonomia,cap,custo,impacto,localizacao,reabastecimento))
          
     return carros


def gerar_pedidos(nr_pedidos):
     pedidos = []
     for _ in range(nr_pedidos):
          origem = pontos_coleta[random.randint(0,len(pontos_coleta)-1)]
          destino = origem
          while destino == origem:
               destino = pontos_coleta[random.randint(0,len(pontos_coleta)-1)] # evitar pedidos estupidos
          passageiros = random.randint(1,5)
          prioridade = round(random.randint(1,5)) == 1 # 20% pedidos urgentes! 
          ambiental = round(random.randint(1,5)) == 1 # 20% pedidos vegans 
          if prioridade:
               tempo_espera = random.randint(5,15)
          else:
               tempo_espera = random.randint(15,30) # pedidos normais têm horário mais alargado

          pedidos.append(Pedido(origem,destino,passageiros,prioridade,ambiental,tempo_espera))
     
     return pedidos

# Gera CSVs
def main():
    carros = gerar_frota(15,30)
    pedidos = gerar_pedidos(1000)
    with open('data/Veiculos.csv', 'w', newline='') as file:
        escritor = csv.writer(file, delimiter=',')
        for carro in carros:
            escritor.writerow(carro.serialize_carro())
    print("Veículos gerados!")
    with open('data/Pedidos.csv', 'w', newline='') as file:
        escritor = csv.writer(file, delimiter=',')
        for pedido in pedidos:
            escritor.writerow(pedido.serialize_pedido())
    print("Pedidos gerados!")


if __name__ == "__main__":
    main()