

class Simulador:
     def __init__(self, gestor_frota, gestor_pedidos, hora_inicial):
          self.gestor_frota = gestor_frota
          self.gestor_pedidos = gestor_pedidos
          self.tempo = hora_inicial