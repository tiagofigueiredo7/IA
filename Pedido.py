import Localizacao

class Pedido:
     def __init__(self, 
                  origem: 'Localizacao',
                  destino: 'Localizacao',
                  capacidadePassageiros, 
                  horario, 
                  prioridade, 
                  preferenciaAmbiental
                  ):
          self.origem = origem
          self.destino = destino
          self.capacidadePassageiros = capacidadePassageiros
          self.horario = horario
          self.prioridade = prioridade
          self.preferenciaAmbiental = preferenciaAmbiental

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

     def __str__(self):
          return f"Pedido de {self.capacidadePassageiros} passageiros de {self.origem.getName()} para {self.destino.getName()} às {self.horario}, Prioridade: {self.prioridade}, Preferência Ambiental: {self.preferenciaAmbiental}"
     
     
     