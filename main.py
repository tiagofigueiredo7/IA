
from classes.Carro import Carro
from classes.Pedido import Pedido
from classes.Hora import Hora
from parsers import parser

def main():
     
     ## parse de dados

     carros, pedidos = parser( "data/Carros.csv", "data/Pedidos.csv")

     tempo = Hora(0,0)

     while (True):
          ## gera trafego na cidade quando chegam horas de ponta

          ##adicionaPedidos(pedidos)
          ## logica principal 
          ## tem um ciclo que gera um random 'x' entre 5 e 10 ( ou qq intervalo de valores ) 
          # e adiciona 'x' Pedidos à lista de Pedidos ativa

          tempo.incrementaMinuto()

          break

          
          

     ## calcula métricas
     ## temos de guardar os tempos, consumos e assim .....

     print("Hello, World!")


if __name__ == "__main__":
    main()