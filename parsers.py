import csv
from classes.Carro import Carro
from classes.Pedido import Pedido
from queue import deque

def parser_cars(file_path):
     cars = {} ## dicionario de carros, aka Map (O(1) para adicionar e remover)
     with open(file_path, 'r') as file:
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               carro = Carro.parse_car(linha)
               cars[carro.getID()] = carro
     return cars

def parser_pedidos(file_path):
     pedidos = deque() ## deque de pedidos, aka Queue (0(1) para adicionar e remover)
     with open(file_path , 'r') as file:    ## 'r' para modo de leitura
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               pedido = Pedido.parse_pedido(linha)
               pedidos.append(pedido)
     return pedidos

def parser(ficheiro_carros, ficheiro_pedidos):

     carros = parser_cars(ficheiro_carros)
     pedidos = parser_pedidos(ficheiro_pedidos)

     return carros, pedidos