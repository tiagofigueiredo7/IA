class Carro:
     def __init__(
        self, 
        id,
        tipo,
        autonomia_max, 
        capacidade_passageiros,
        custo_km,
        impacto_ambiental,
        localizacao,
        tempo_reabastecimento
     ):
        self.id = id
        self.tipo = tipo
        self.autonomia_max = autonomia_max
        self.autonomia_atual = autonomia_max 
        self.capacidade_passageiros = capacidade_passageiros
        self.custo_km = custo_km
        self.impacto_ambiental = impacto_ambiental
        self.localizacao = localizacao
        self.tempo_reabastecimento = tempo_reabastecimento
        self.rota = []
        self.tempo_rota = [] 
        self.passageiros = [] ### nr passageiros em cada local

     def getID(self):
          return self.id

     def getTipo(self):
          return self.tipo
     
     def getAutonomiaMax(self):
          return self.autonomia_max
     
     def getAutonomiaAtual(self):
          return self.autonomia_atual
     
     def getCapacidadePassageiros(self):
          return self.capacidade_passageiros
     
     def getCustoKM(self):
          return self.custo_km
     
     def getImpactoAmbiental(self):
          return self.impacto_ambiental
     
     def getLocalizacao(self):
          return self.localizacao
     
     def getTempoReabastecimento(self):
          return self.tempo_reabastecimento
     
     def getTempoAteDisponivel(self):
          td = 0
          for t in self.tempo_rota:
               td += t 
          return td
     
     def getNrPassageiros(self):
          if len(self.passageiros) > 0:
               return self.passageiros[0]
          return 0
     
     def getRota(self):
          return list(zip(self.rota,self.tempo_rota,self.passageiros))
     
     def getFimDaRota(self):
          if len(self.rota) > 0:
               return self.rota[-1]
          return self.localizacao
     
     def setID(self, id):
          self.id = id
     
     def setTipo(self, tipo):
          self.tipo = tipo

     def setAutonomiaMax(self, autonomiamax):
          self.autonomia_max = autonomiamax
     
     def setAutonomiaAtual(self, autonomiatual):
          self.autonomia_atual = autonomiatual
     
     def setCapacidadePassageiros(self, capacidade):
          self.capacidade_passageiros = capacidade
     
     def setCustoKM(self, custokm):
          self.custo_km = custokm
     
     def setImpactoAmbiental(self, impactoAmbiental):
          self.impacto_ambiental = impactoAmbiental

     def setLocalizacao(self, localizacao):
          self.localizacao = localizacao

     # atualiza rota do veículo
     def setRota(self, rota, tempo, nr_passageiros, origem):
          start = len(self.rota)
          if start > 0:
               self.rota.pop()
               tempo[0] += self.tempo_rota.pop()
               start -= 1

          self.rota += rota
          self.tempo_rota += tempo
          self.passageiros += ([0] * len(rota))
          if nr_passageiros > 0:
               self.incNrPassageiros(nr_passageiros,origem,rota[-1],start)
          
          if len(self.rota) != len(self.tempo_rota):
               print(self.rota)
               print(self.tempo_rota)

     # usado no caso de boleia partilhada, para alterar nr de passageiros que entram ou saem
     def incNrPassageiros(self, nr: int, origem:str, destino:str, start: int):
          entrada = self.rota.index(origem,start)
          saida = self.rota.index(destino,entrada+1)
          for i in range(entrada,saida):
               self.passageiros[i] += nr 

     # se passageiro se encontrar na rota do veículo, devolve o tempo que demora a apanhá-lo
     def naRota(self, path: list, nr_passageiros: int):
          if len(self.rota) > len(path):
               t = 0
               for i in range(len(self.rota)-len(path)+1):
                    if self.rota[i:i+len(path)] == path and [(p+nr_passageiros)<=self.capacidade_passageiros for p in (self.passageiros[i:i+len(path)])]:
                         return t
                    else:
                         t += self.tempo_rota[i]
          return -1

     # passa um minuto - atualiza rota e tempo até veículo se encontrar disponível
     def decTempoAteDisponivel(self):
          if len(self.rota) > 0:     
               if self.tempo_rota[0] > 1:
                    self.tempo_rota[0] -= 1
               else:
                    self.rota.pop(0)
                    self.tempo_rota.pop(0)
                    self.passageiros.pop(0)
                    if len(self.rota) > 0:
                         self.localizacao = self.rota[0] ## atualizar localização do veículo
     
     def disponivel(self):
          return len(self.rota) == 0

     def __str__(self):
          return f"Carro {self.tipo} (ID: {self.id}, Autonomia Max: {self.autonomia_max}, Autonomia Atual: {self.autonomia_atual}, Capacidade Passageiros: {self.capacidade_passageiros}, Custo KM: {self.custo_km}, Impacto Ambiental: {self.impacto_ambiental}, Localizacao: {self.localizacao}, Tempo Reabastecimento: {self.tempo_reabastecimento})"
     
     def reabastecer(self):
          self.autonomia_atual = self.autonomia_max
     
     @staticmethod
     def parse_car(linha):
          id = linha[0]
          tipo = linha[1]
          autonomia_max = float(linha[2])
          capacidade = int(linha[3])
          custo_km = float(linha[4])
          impacto_ambiental = float(linha[5])
          localizacao = linha[6]
          reabastecimento = int(linha[7])

          return Carro(id,tipo,autonomia_max,capacidade,custo_km,impacto_ambiental,localizacao,reabastecimento)
     
     def serialize_carro(self):
          return [self.id,
               self.tipo,
               self.autonomia_max,
               self.capacidade_passageiros,
               self.custo_km,
               self.impacto_ambiental,
               self.localizacao,
               self.tempo_reabastecimento]
