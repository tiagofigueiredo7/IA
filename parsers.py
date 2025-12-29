import csv
from classes.Carro import Carro
from classes.Pedido import Pedido

def parser_cars(file_path):
     cars = []
     with open(file_path, 'r') as file:
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               cars.append(Carro.parse_car(linha))
     return cars

def parser_pedidos(file_path):
     pedidos = []
     with open(file_path , 'r') as file:    ## 'r' para modo de leitura
          leitor = csv.reader(file, delimiter= ',')
          for linha in leitor:
               pedidos.append(Pedido.parse_pedido(linha))
     return pedidos

def parser(ficheiro_carros, ficheiro_pedidos):
     carros = parser_cars(ficheiro_carros)
     pedidos = parser_pedidos(ficheiro_pedidos)
     
     return carros, pedidos