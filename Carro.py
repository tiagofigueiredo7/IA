import Localizacao

# Classe Carro

class Carro:
     def __init__(
        self, 
        tipo_combustivel,
        autonomia_max, 
        autonomia_atual, 
        capacidade_passageiros,
        custo_km,
        impacto_ambiental,
        disponibilidade,
        localizacao: 'Localizacao',
        tempo_reabastecimento
     ):
        self.tipo_combustivel = tipo_combustivel
        self.autonomia_max = autonomia_max
        self.autonomia_atual = autonomia_atual
        self.capacidade_passageiros = capacidade_passageiros
        self.custo_km = custo_km
        self.impacto_ambiental = impacto_ambiental
        self.disponibilidade = disponibilidade
        self.localizacao = localizacao
        self.tempo_reabastecimento = tempo_reabastecimento

     def getTipoCombustivel(self):
          return self.tipo_combustivel
     
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
     
     def getTempoReabastecimento (self):
          return self.tempo_reabastecimento
     
     def setTipoCombustivel(self, tipocombustivel):
          self.tipo_combustivel = tipocombustivel

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

     def __str__(self):
          return f"Carro(tipo_combustivel={self.tipo_combustivel}, autonomia_max={self.autonomia_max}, autonomia_atual={self.autonomia_atual}, capacidade_passageiros={self.capacidade_passageiros}, custo_km={self.custo_km}, impacto_ambiental={self.impacto_ambiental}, disponibilidade={self.disponibilidade}, localizacao={self.localizacao}, tempo_reabastecimento={self.tempo_reabastecimento})"
     
     def reabastecer(self):
          self.autonomia_atual = self.autonomia_max

     def is_disponivel(self):
          return self.disponibilidade
     
     def atualizar_localizacao(self, nova_localizacao: 'Localizacao'):
          self.localizacao = nova_localizacao
     