import networkx as nx 
import matplotlib.pyplot as plt
from classes.Tipo_Localizacao import Tipo_Localizacao as tl
from classes.Localizacao import Localizacao 


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
        self.adicionar_ponto("Aguiar", tl.Ponto_Coleta)
        self.adicionar_ponto("Balugães", tl.Ponto_Coleta)
        self.adicionar_ponto("Chorente", tl.Ponto_Coleta)
        self.adicionar_ponto("Alvito", tl.Ponto_Coleta)
        self.adicionar_ponto("Panque", tl.Ponto_Coleta)
        
        self.adicionar_ponto("BP 1", tl.Posto_Combustivel)
        self.adicionar_ponto("Galp 1", tl.Posto_Combustivel)
        self.adicionar_ponto("Moeve 1", tl.Posto_Combustivel)
        self.adicionar_ponto("Shell 1", tl.Posto_Combustivel)
        self.adicionar_ponto("Repsol 1", tl.Posto_Combustivel)
        self.adicionar_ponto("BP 2", tl.Posto_Combustivel)
        self.adicionar_ponto("Galp 2", tl.Posto_Combustivel)
        self.adicionar_ponto("Moeve 2", tl.Posto_Combustivel)
        self.adicionar_ponto("Shell 2", tl.Posto_Combustivel)
        self.adicionar_ponto("Repsol 2", tl.Posto_Combustivel)

        self.adicionar_ponto("Mercadona 1", tl.Estacao_Carregamento)
        self.adicionar_ponto("Intermarche 1", tl.Estacao_Carregamento)
        self.adicionar_ponto("Mercadona 2", tl.Estacao_Carregamento)
        self.adicionar_ponto("Intermarche 2", tl.Estacao_Carregamento)
        self.adicionar_ponto("Mercadona 3", tl.Estacao_Carregamento)
        self.adicionar_ponto("Intermarche 3", tl.Estacao_Carregamento)
        self.adicionar_ponto("Campo da Feira", tl.Estacao_Carregamento)

        self.adicionar_caminho("Barcelos","Arcozelo", 1)
        self.adicionar_caminho("Barcelos","Barcelinhos", 2)
        self.adicionar_caminho("Barcelos","Vila Boa", 3)
        self.adicionar_caminho("Barcelos","Rio Covo", 5)
        self.adicionar_caminho("Barcelos","Vila Frescainha", 5)
        self.adicionar_caminho("Vila Boa", "Arcozelo", 3)
        self.adicionar_caminho("Vila Boa", "Lijó", 5)
        self.adicionar_caminho("Rio Covo", "Várzea", 2)
        self.adicionar_caminho("Rio Covo", "Barcelinhos", 6)
        self.adicionar_caminho("Barcelinhos","Vila Frescainha", 2)
        self.adicionar_caminho("Lijó","Silva", 4)
        self.adicionar_caminho("Lijó","Arcozelo", 5)
        self.adicionar_caminho("Aguiar","Balugães",4)
        self.adicionar_caminho("Panque","Alvito",2)
        self.adicionar_caminho("Chorente","Panque",1)
        self.adicionar_caminho("Panque","Vila Frescainha",6)
        self.adicionar_caminho("Alvito","Vila Frescainha",3)
        self.adicionar_caminho("Aguiar","Panque",5)
        self.adicionar_caminho("Várzea","Alvito",2)

        self.adicionar_caminho("Vila Boa", "BP 1", 1)
        self.adicionar_caminho("Barcelos", "Galp 1", 5)
        self.adicionar_caminho("Várzea", "Moeve 1", 3)
        self.adicionar_caminho("Rio Covo", "Moeve 1", 2)
        self.adicionar_caminho("Silva", "Shell 1", 4)
        self.adicionar_caminho("Barcelinhos", "Repsol 1", 2)
        self.adicionar_caminho("Lijó", "BP 1", 3)
        self.adicionar_caminho("Alvito", "Galp 2", 3)
        self.adicionar_caminho("Balugães", "BP 2", 4)
        self.adicionar_caminho("Panque", "Moeve 2", 2)
        self.adicionar_caminho("Chorente", "Shell 2", 1)
        self.adicionar_caminho("Aguiar", "Repsol 2", 2) 
        self.adicionar_caminho("Aguiar","Silva",5)
        self.adicionar_caminho("Balugães","Chorente",6)

        self.adicionar_caminho("Barcelos", "Mercadona 1", 5)
        self.adicionar_caminho("Chorente", "Intermarche 2",2)
        self.adicionar_caminho("Silva","Intermarche 3",4)
        self.adicionar_caminho("Barcelos", "Intermarche 1", 5)
        self.adicionar_caminho("Barcelos", "Campo da Feira", 1)
        self.adicionar_caminho("Aguiar", "Mercadona 2", 4)
        self.adicionar_caminho("Panque", "Mercadona 3", 6)
        self.adicionar_caminho("Lijó","Mercadona 3", 4)
        self.adicionar_caminho("Vila Frescainha", "Intermarche 2", 3)
        self.adicionar_caminho("Arcozelo", "Campo da Feira", 3)

    # Devolve lista dos locais da cidade
    def getLocais(self):
        lista = []
        for l in self.locais:
            lista.append(l.getName())
        return lista

    # adiciona ponto à cidade
    def adicionar_ponto(self, nome, tipo): # id determinado pela cidade
        id = len(self.locais) + 1
        p = Localizacao(nome,id,tipo)
        self.locais.append(p)
        self.vizinhos[nome] = []

    # adiciona o caminho entre dois pontos na cidade
    def adicionar_caminho(self, ponto1, ponto2, distancia):
        self.vizinhos[ponto1].append((ponto2, distancia)) 
        self.vizinhos[ponto2].append((ponto1, distancia))
    
    # procura um local pelo nome
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

    # calcula a distância e tempo esperado de um caminho
    def calcular_distancia_tempo(self, caminho): # caminho é uma lista de nodos
        d = 0
        t = 0
        for i in range(0,len(caminho)-1):
            d = d + self.get_distancia(caminho[i], caminho[i + 1])
            t = t + self.get_distancia(caminho[i], caminho[i + 1]) + (self.get_transito(caminho[i])/2)
        return d, t
    
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
        self.transito[local] = estima
    
    def get_transito(self, local):
        if local not in self.transito:
            self.transito[local] = len(self.vizinhos[local]) ### transito em função do nr de vizinhos?
        return self.transito[local]