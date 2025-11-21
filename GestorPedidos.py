import random
from classes.Pedido import Pedido

class GestorPedidos:
     def __init__(self):
          self.pedidosAtivos = {
          "alta": [],
          "media": [],
          "baixa": []
     }

     def adicionaPedidos(self, novos_pedidos):
          num_pedidos = random.randint(5, 10)
          for _ in range(num_pedidos):
               if novos_pedidos:
                    pedido = novos_pedidos.popleft()
                    prioridade = pedido.getPrioridade()
                    self.pedidosAtivos[prioridade].append(pedido)

     def getPedidosAtivos(self):
          return self.pedidosAtivos