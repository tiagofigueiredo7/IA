from classes.Tipo_Localizacao import Tipo_Localizacao

class Localizacao:
     def __init__(self, nome, id, tipo: Tipo_Localizacao):
          self.nome = nome
          self.id = id
          self.tipo = tipo 

     def getName(self):
          return self.nome

     def getId(self):
          return self.id
     
     def getTipo(self):
          return self.tipo
     
     def setName(self, nome):
          self.nome = nome

     def setId(self, id):
          self.id = id

     def setTipo(self, tipo: Tipo_Localizacao):
          self.tipo = tipo

     def __eq__(self, other):
          return self.id == other.id ## comparação pelo nome
     
     def __str__(self):
          return f"Localizacao(Nome: {self.nome}, ID: {self.id}, Tipo: {self.tipo})"
     
     @staticmethod
     def parse_localizacao(linha):
          nome = linha[0]
          id = linha[1]
          tipo = Tipo_Localizacao[linha[2]]

          return Localizacao(nome, id, tipo)