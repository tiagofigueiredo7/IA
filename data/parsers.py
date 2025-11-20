
from Carro import Carro
from Pedido import Pedido
from queue import deque

from csv import csv

def parser_cars(file_path):
     cars = {} ## dicionario de carros, aka Map (O(1) para adicionar e remover)
     with open(file_path, 'r') as file:
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               carro = parse_car(linha)
               cars[carro.getID] = carro
     return cars

def parser_pedidos(file_path):
     pedidos = deque() ## deque de pedidos, aka Queue (0(1) para adicionar e remover)
     with open(file_path , 'r') as file:    ## 'r' para modo de leitura
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               pedido = parse_pedido(linha)
               pedidos.append(pedido)
     return pedidos

def parser_clientes(file_path):
     clientes = {}
     with open(file_path, 'r') as file:
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               cliente = parse_cliente(linha)
               clientes[cliente.getID] = cliente
     return clientes

def parser(ficheiro_carros, ficheiro_pedidos, ficheiro_clientes, ficheiro_cidade): 

     carros = parser_cars(ficheiro_carros)
     pedidos = parser_pedidos(ficheiro_pedidos)
     clientes = parser_clientes(ficheiro_clientes)
     cidade = parser_mapa(ficheiro_cidade)

     return carros, pedidos, clientes, cidade