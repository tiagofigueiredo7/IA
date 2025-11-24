from .Localizacao import Localizacao

class Pedido:
     def __init__(self,
                  origem,
                  destino,
                  numPassageiros: int,
                  prioridade: bool,
                  preferenciaAmbiental: bool,
                  tempoEsperaMax: int ):
          self.origem = origem
          self.destino = destino
          self.numPassageiros = numPassageiros
          self.prioridade = prioridade
          self.preferenciaAmbiental = preferenciaAmbiental
          self.tempoEsperaMax = tempoEsperaMax

     def getOrigem(self):
          return self.origem
     
     def getDestino(self):
          return self.destino
     
     def getNumPassageiros(self):
          return self.numPassageiros
     
     def getPrioridade(self):
          return self.prioridade
     
     def getPreferenciaAmbiental(self):
          return self.preferenciaAmbiental
     
     def getTempoEsperaMax(self):
          return self.tempoEsperaMax

     # à passagem de um minuto, decrementa o tempo de espera max do pedido
     def decTempoEsperaMax(self):
          self.tempoEsperaMax = self.tempoEsperaMax -1
          if self.tempoEsperaMax <= 0:
               return False ### pedido n foi respondido a tempo 
          return True
          

     def __str__(self):
          origem = str(self.origem)
          destino = str(self.destino)
          return f"Pedido(Origem: {origem}, Destino: {destino}, NumPassageiros: {self.numPassageiros}, Prioridade: {self.prioridade}, PreferenciaAmbiental: {self.preferenciaAmbiental}, TempoEsperaMax: {self.tempoEsperaMax})"
     
     @staticmethod
     def parse_pedido(linha):
          origem = linha[0]
          #origem = Localizacao.parse_localizacao(linha[0:3])
          destino = linha[1]
          #destino = Localizacao.parse_localizacao(linha[3:6])
          numPassageiros = int(linha[2])
          #numPassageiros = int(linha[6])
          #prioridade = linha[7]
          prioridade = linha[3].lower() == 'alta'
          #preferenciaAmbiental = linha[8].lower() == 'true'
          preferenciaAmbiental = linha[4].lower() == 'true'
          #tempoEsperaMax = int(linha[9])
          tempoEsperaMax = int(linha[5])

          return Pedido(origem, destino, numPassageiros, prioridade, preferenciaAmbiental, tempoEsperaMax)