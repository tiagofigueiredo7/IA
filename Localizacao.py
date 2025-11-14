

class Localizacao:
     def __init__(self, nome, id):
          self.nome = nome
          self.id = id

     def getName(self):
          return self.nome

     def getId(self):
          return self.id
     
     def setName(self, nome):
          self.nome = nome

     def setId(self, id):
          self.id = id

     def __eq__(self, other):
          return self.nome == other.nome ## comparação pelo nome    
     
     def __hash__(self):
          return hash(self.nome)
     
     def __str__(self):
          return "node " + self.nome