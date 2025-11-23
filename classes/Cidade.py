from Localizacao import Localizacao
from Tipo_Localizacao import Tipo_Localizacao as tl

import networkx as nx 
import matplotlib.pyplot as plt 


class Cidade:
    def __init__(self):
        self.locais = []   # lista de pontos da cidade
        self.vizinhos = {} # dicionário (key = nome dum ponto, value = lista de pontos vizinhos (pontos com caminho direto))
        self.transito = {} # dicionario (key = nome dum ponto, value = trânsito nesse ponto) 
        
        # aqui define-se a cidade, dps inventar mais...
        self.adicionar_ponto("Arcozelo", tl.Ponto_Coleta)
        self.adicionar_ponto("Barcelos", tl.Ponto_Coleta)
        self.adicionar_ponto("Rio Covo", tl.Ponto_Coleta)
        self.adicionar_ponto("Barcelinhos", tl.Ponto_Coleta)
        self.adicionar_ponto("Vila Boa", tl.Ponto_Coleta)
        self.adicionar_ponto("Silva", tl.Ponto_Coleta)
        self.adicionar_ponto("Lijó", tl.Ponto_Coleta)
        self.adicionar_ponto("Vila Frescainha", tl.Ponto_Coleta)
        self.adicionar_ponto("Várzea", tl.Ponto_Coleta)
        
        self.adicionar_ponto("BP", tl.Posto_Combustivel)
        self.adicionar_ponto("Galp", tl.Posto_Combustivel)
        self.adicionar_ponto("Moeve", tl.Posto_Combustivel)
        self.adicionar_ponto("Shell", tl.Posto_Combustivel)
        self.adicionar_ponto("Repsol", tl.Posto_Combustivel)

        self.adicionar_ponto("Mercadona", tl.Estacao_Carregamento)
        self.adicionar_ponto("Intermarche", tl.Estacao_Carregamento)
        self.adicionar_ponto("Campo da Feira", tl.Estacao_Carregamento)

        self.adicionar_caminho("Barcelos","Arcozelo", 1)
        self.adicionar_caminho("Barcelos","Barcelinhos", 2)
        self.adicionar_caminho("Barcelos","Vila Boa", 3)
        self.adicionar_caminho("Barcelos","Rio Covo", 5)
        self.adicionar_caminho("Barcelos","Vila Frescainha", 5)
        self.adicionar_caminho("Vila Boa", "Arcozelo", 3)
        self.adicionar_caminho("Vila Boa", "Lijó", 5)
        self.adicionar_caminho("Rio Covo", "Várzea", 7)
        self.adicionar_caminho("Rio Covo", "Barcelinhos", 6)
        self.adicionar_caminho("Barcelinhos","Vila Frescainha", 2)
        self.adicionar_caminho("Lijó","Silva", 4)
        self.adicionar_caminho("Lijó","Arcozelo", 5)

        self.adicionar_caminho("Vila Boa", "BP", 1)
        self.adicionar_caminho("Barcelos", "Galp", 5)
        self.adicionar_caminho("Várzea", "Moeve", 3)
        self.adicionar_caminho("Rio Covo", "Moeve", 2)
        self.adicionar_caminho("Silva", "Shell", 4)
        self.adicionar_caminho("Barcelinhos", "Repsol", 2)

        self.adicionar_caminho("Barcelos", "Mercadona", 5)
        self.adicionar_caminho("Barcelos", "Intermarche", 5)
        self.adicionar_caminho("Barcelos", "Campo da Feira", 1)
        self.adicionar_caminho("Vila Frescainha", "Intermarche", 3)
        self.adicionar_caminho("Arcozelo", "Campo da Feira", 3)


    # adiciona ponto à cidade
    def adicionar_ponto(self, nome, tipo): # id determinado pela cidade
        id = len(self.locais)
        p = Localizacao(nome,id,tipo)
        self.locais.append(p)
        self.vizinhos[nome] = []

    # adiciona o caminho entre dois pontos na cidade
    def adicionar_caminho(self, ponto1, ponto2, distancia):
        self.vizinhos[ponto1].append((ponto2, distancia)) 
        self.vizinhos[ponto2].append((ponto1, distancia))
    
    # procura um local na cidade pelo nome
    def get_local(self, local):
        for l in self.locais:
            if l.getName() == local:
                return l
        return None
    
    # devolve lista de vizinhos de um local e a sua distância
    def get_vizinhos(self, local):
        lista = []
        for v in self.vizinhos[local]:
            lista.append(v)
        return lista
    
    # devolve a distância entre dois pontos vs, se o forem
    def get_distancia(self, local1, local2):
        for l,d in self.vizinhos[local1]:
            if l == local2:
                return d
        return None

    # calcula a distância de um caminho
    def calcular_distancia(self, caminho): # caminho é uma lista de nodos
        d = 0
        for i in range(0,len(caminho)-1):
            d = d + self.get_distancia(caminho[i], caminho[i + 1])
        return d

    # desenha a cidade
    def desenhar_cidade(self):
        g = nx.Graph()
        for l in self.locais:
            n = l.getName()
            g.add_node(n)
            for v, d in self.vizinhos[n]:
                g.add_edge(n, v, weight=d)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.draw()
        plt.show()

    ####################################################
    # depois ver como fazer para ter trânsito dinâmico #
    ####################################################
    def adicionarTransito(self, local, estima):
        pass
    def get_transito(self, local):
        pass



if __name__ == "__main__":
    c = Cidade()
    c.desenhar_cidade() # para ver como fica a cidade