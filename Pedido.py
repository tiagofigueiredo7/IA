import Localizacao

class Pedido:
     def __init__(self, 
                  origem: 'Localizacao',
                  destino: 'Localizacao',
                  capacidadePassageiros, 
                  horario, 
                  prioridade, 
                  preferenciaAmbiental,
                  cliente ## id do cliente que fez o pedido
                  ):
          self.origem = origem
          self.destino = destino
          self.capacidadePassageiros = capacidadePassageiros
          self.horario = horario ????? que tipo de dados ????? 
          self.prioridade = prioridade
          self.preferenciaAmbiental = preferenciaAmbiental ????? boolean ?????
          self.cliente = cliente

     def getOrigem(self):
          return self.origem

     def getDestino(self):
          return self.destino

     def getCapacidadePassageiros(self):
          return self.capacidadePassageiros

     def getHorario(self):
          return self.horario

     def getPrioridade(self):
          return self.prioridade

     def getPreferenciaAmbiental(self):
          return self.preferenciaAmbiental
     
     def getCliente(self):
          return self.cliente

     def setOrigem(self, origem):
          self.origem = origem

     def setDestino(self, destino):
          self.destino = destino

     def setCapacidadePassageiros(self, capacidadePassageiros):
          self.capacidadePassageiros = capacidadePassageiros

     def setHorario(self, horario):
          self.horario = horario

     def setPrioridade(self, prioridade):
          self.prioridade = prioridade

     def setPreferenciaAmbiental(self, preferenciaAmbiental):
          self.preferenciaAmbiental = preferenciaAmbiental

     def setCliente(self, cliente):
          self.cliente = cliente

     def __str__(self):
          return f"Pedido de {self.capacidadePassageiros} passageiros de {self.origem.getName()} para {self.destino.getName()} às {self.horario}, Prioridade: {self.prioridade}, Preferência Ambiental: {self.preferenciaAmbiental}, Cliente: {self.cliente}"
     
     def parse_pedido(self, linha):
          self.origem = linha[0]
          self.destino = linha[1]
          self.capacidadePassageiros = int(linha[2])
          self.horario = ??????????
          self.prioridade = int(linha[4])
          self.preferenciaAmbiental = linha[5]
          self.cliente = int(linha[6])
