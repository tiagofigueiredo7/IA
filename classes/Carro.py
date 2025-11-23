from Localizacao import Localizacao
from Tipo_Localizacao import Tipo_Localizacao

class Carro:
     def __init__(
        self, 
        id,
        tipo,
        autonomia_max, 
        autonomia_atual, 
        capacidade_passageiros,
        custo_km,
        impacto_ambiental,
        disponibilidade,
        localizacao: Localizacao,
        tempo_reabastecimento
     ):
        self.id = id
        self.tipo = tipo
        self.autonomia_max = autonomia_max
        self.autonomia_atual = autonomia_atual 
        self.capacidade_passageiros = capacidade_passageiros
        self.custo_km = custo_km
        self.impacto_ambiental = impacto_ambiental
        self.disponibilidade = disponibilidade
        self.localizacao = localizacao
        self.tempo_reabastecimento = tempo_reabastecimento
        self.tempo_ate_disponibilidade = 0

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
     
     def getDisponibilidade(self):
          return self.disponibilidade
     
     def getLocalizacao(self):
          return self.localizacao
     
     def getTempoReabastecimento(self):
          return self.tempo_reabastecimento
     
     def getTempoAteDisponivel(self):
          return self.tempo_ate_disponibilidade
     
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

     def setTempoAteDisponivel(self, t):
          self.tempo_ate_disponibilidade = t

     def __str__(self):
          return f"Carro(ID: {self.id}, Tipo: {self.tipo}, Autonomia Max: {self.autonomia_max}, Autonomia Atual: {self.autonomia_atual}, Capacidade Passageiros: {self.capacidade_passageiros}, Custo KM: {self.custo_km}, Impacto Ambiental: {self.impacto_ambiental}, Disponibilidade: {self.disponibilidade}, Localizacao: {self.localizacao}, Tempo Reabastecimento: {self.tempo_reabastecimento})"
     
     def reabastecer(self):
          self.autonomia_atual = self.autonomia_max

     def is_disponivel(self):
          return self.disponibilidade
     
     def atualizar_localizacao(self, nova_localizacao: Localizacao):
          self.localizacao = nova_localizacao
     
     @staticmethod
     def parse_car(linha):
          id = linha[0]
          tipo = linha[1]
          autonomia_max = float(linha[2])
          autonomia_atual = float(linha[3]) ## em vez de ser parte do CSV podiamos assumir q o deposito está cheio inicialmente
          capacidade_passageiros = int(linha[4])
          custo_km = float(linha[5])
          impacto_ambiental = float(linha[6])
          disponibilidade = linha[7].lower() == 'true' ## se separarmos carros por disponibilidade n será necessario

          localizacao = Localizacao.parse_localizacao(linha[8:11])

          tempo_reabastecimento = int(linha[11])

          return Carro(
               id,
               tipo,
               autonomia_max,
               autonomia_atual,
               capacidade_passageiros,
               custo_km,
               impacto_ambiental,
               disponibilidade,
               localizacao,
               tempo_reabastecimento
          )
