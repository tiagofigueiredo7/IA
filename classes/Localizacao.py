from classes.Tipo_Localizacao import Tipo_Localizacao

class Localizacao:
     def __init__(self, nome, tipo: Tipo_Localizacao):
          self.nome = nome
          self.tipo = tipo 

     def getName(self):
          return self.nome
     
     def getTipo(self):
          return self.tipo
     
     def setName(self, nome):
          self.nome = nome

     def setTipo(self, tipo: Tipo_Localizacao):
          self.tipo = tipo

     def __eq__(self, other):
          return self.nome == other.nome
     
     def __str__(self):
          return f"Localizacao(Nome: {self.nome}, Tipo: {self.tipo})"