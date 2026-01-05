import networkx as nx 
import matplotlib.pyplot as plt
import random as rd
from classes.Tipo_Localizacao import Tipo_Localizacao as tl
from classes.Localizacao import Localizacao 
from classes.Hora import Hora


class Cidade:
    def __init__(self):
        self.locais = []   # lista de pontos da cidade
        self.vizinhos = {} # dicionário (key = nome dum ponto, value = lista de pontos vizinhos (pontos com caminho direto))
        self.transito = {} # dicionario (key = nome dum ponto, value = trânsito nesse ponto) 
        self.cache = {}

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
        self.adicionar_caminho("Vila Boa", "Lijó", 1)
        self.adicionar_caminho("Rio Covo", "Várzea", 2)
        self.adicionar_caminho("Rio Covo", "Barcelinhos", 6)
        self.adicionar_caminho("Barcelinhos","Vila Frescainha", 2)
        self.adicionar_caminho("Lijó","Silva", 4)
        self.adicionar_caminho("Lijó","Arcozelo", 3)
        self.adicionar_caminho("Aguiar","Balugães",4)
        self.adicionar_caminho("Panque","Alvito",5)
        self.adicionar_caminho("Chorente","Panque",3)
        self.adicionar_caminho("Panque","Vila Frescainha",6)
        self.adicionar_caminho("Alvito","Vila Frescainha",3)
        self.adicionar_caminho("Aguiar","Panque",4)
        self.adicionar_caminho("Várzea","Alvito",2)
        self.adicionar_caminho("Aguiar","Silva",7)
        self.adicionar_caminho("Balugães","Chorente",9)

        self.adicionar_caminho("Vila Boa", "BP 1", 1)
        self.adicionar_caminho("Barcelos", "Galp 1", 1)
        self.adicionar_caminho("Várzea", "Moeve 1", 3)
        self.adicionar_caminho("Rio Covo", "Moeve 1", 2)
        self.adicionar_caminho("Silva", "Shell 1", 4)
        self.adicionar_caminho("Barcelinhos", "Repsol 1", 2)
        self.adicionar_caminho("Lijó", "BP 1", 3)
        self.adicionar_caminho("Alvito", "Galp 2", 1)
        self.adicionar_caminho("Balugães", "BP 2", 4)
        self.adicionar_caminho("Panque", "Moeve 2", 2)
        self.adicionar_caminho("Chorente", "Shell 2", 1)
        self.adicionar_caminho("Aguiar", "Repsol 2", 2) 

        self.adicionar_caminho("Barcelos", "Mercadona 1", 1)
        self.adicionar_caminho("Chorente", "Intermarche 2",2)
        self.adicionar_caminho("Silva","Intermarche 3",4)
        self.adicionar_caminho("Barcelos", "Intermarche 1", 3)
        self.adicionar_caminho("Barcelos", "Campo da Feira", 1)
        self.adicionar_caminho("Aguiar", "Mercadona 2", 4)
        self.adicionar_caminho("Panque", "Mercadona 3", 3)
        self.adicionar_caminho("Lijó","Mercadona 3", 2)
        self.adicionar_caminho("Vila Frescainha", "Intermarche 2", 3)
        self.adicionar_caminho("Arcozelo", "Campo da Feira", 2)
        
        for l,v in self.vizinhos.items():
            self.set_transito(l,round(len(v)/2))

        self.clima = {} # clima definido para o dia
        for h in range(24): ## em cada hora, caso o clima seja mau, o transito pode dobrar
            if rd.randint(1,5) == 5: # 20% probabilidade de mau tempo
                self.clima[h] = 2
            else:
                self.clima[h] = 1


    # Devolve lista dos locais/pontos da cidade
    def getLocais(self):
        lista = []
        for l in self.locais:
            lista.append(l.getName())
        return lista
    
    # Devolve lista dos pontos de coleta de passageiros da cidade
    def getPontosColeta(self):
        lista = []
        for l in self.locais:
            if l.getTipo() == tl.Ponto_Coleta:
                lista.append(l.getName())
        return lista

    # Adiciona ponto/local à cidade
    def adicionar_ponto(self, nome, tipo):
        p = Localizacao(nome,tipo)
        self.locais.append(p)
        self.vizinhos[nome] = []
        self.cache[nome] = dict() ## dicionário para adicionar rotas a partir deste local

    # Adiciona o caminho entre dois pontos na cidade
    def adicionar_caminho(self, ponto1, ponto2, distancia):
        self.vizinhos[ponto1].append((ponto2, distancia)) 
        self.vizinhos[ponto2].append((ponto1, distancia))
    
    # Procura um local pelo nome
    def get_local(self, local):
        for l in self.locais:
            if l.getName() == local:
                return l
        return None

    # Devolve lista de vizinhos de um local e a sua distância
    def get_vizinhos(self, local):
        lista = []
        for v in self.vizinhos[local]:
            lista.append(v)
        return lista
    
    # Devolve a distância entre dois pontos vizinhos, se o forem
    def get_distancia(self, local1, local2):
        for l,d in self.vizinhos[local1]:
            if l == local2:
                return d
        return None

    # Calcula a distância e tempo esperado de um caminho
    def calcular_distancia_tempo(self, caminho: list, h: Hora, tempo_extra: int): # caminho é uma lista de nodos
        d = 0
        t = [] # lista com o tempo que vai ficar em cada ponto da rota 
        if len(caminho) > 0:
            for i in range(len(caminho)-1):
                aux = self.get_distancia(caminho[i], caminho[i + 1])
                d += aux
                # tempo = distantância até próximo ponto + trânsito
                t.append(aux + (self.get_transito_atual(caminho[i],h)))
            t.append(tempo_extra)
        return d, t
    
    # Desenha a cidade
    def desenhar_cidade(self):
        g = nx.Graph()
        for l in self.locais:
            n = l.getName()
            g.add_node(n)
            for v, d in self.vizinhos[n]:
                g.add_edge(n, v, weight=d)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, arrows=True, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.draw()
        plt.show()

    # Adiciona trânsito a um local
    def set_transito(self, local, estima):
        self.transito[local] = estima

    # Devolve trânsito mínimo de um local 
    def get_transito(self, local: str):
        return self.transito[local]

    # Devolve trânsito de um local a uma dada hora 
    def get_transito_atual(self, local: str, hora: Hora):
        t = self.transito[local]
        if hora.eHoraPonta(): # é o dobro em hora de ponta
            t = t * 2
        return t * (self.clima[hora.getHora()]) # pode dobrar, se estiver mau tempo
    
    # Adiciona caminho à cache para não ter de ser recalculado
    def add_to_cache(self, inicio: str, fim: str, path: list):
        (self.cache[inicio])[fim] = path
    
    # Limpa a cache para iniciar nova simulação
    def clear_cache(self):
        for k in self.cache.keys():
            self.cache[k] = dict()

    # Se está mau tempo em dada hora
    def mau_tempo(self, h:Hora):
        return self.clima[h.getHora()] == 2