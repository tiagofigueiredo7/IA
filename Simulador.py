from threading import Thread, Event
from classes.Cidade import Cidade
from classes.Hora import Hora
from algoritmos import BFS, DFS, greedy, aStar
import random

from classes.Pedido import Pedido


class Simulador:
     def __init__(self, veiculos, pedidos, hora_inicial: Hora, cidade: Cidade, algoritmo):
          self.veiculos_disponiveis = veiculos
          self.veiculos_ocupados = {}
          self.pedidos_por_adicionar = pedidos
          self.pedidos_por_responder = {"prioritários": [], "normais": []}
          self.tempo = hora_inicial
          self.cidade = cidade
          self.algoritmo = algoritmo
          
          ## estatísticas
          self.pedidos_respondidos = 0
          self.pedidos_rejeitados = 0
          self.tempo_resposta_total = 0
          self.emissoes_total = 0
          self.custos_operacionais_total = 0
          self.km_sem_passageiros = 0
          ### como fazer taxa de ocupação da frota??


     # Adiciona entre 0 a 5 pedidos ao sistema
     def adicionaPedidos(self):
          num_pedidos = random.randint(0,5)
          if len(self.pedidos_por_adicionar) > 0 and num_pedidos > 0:
               for _ in range(num_pedidos):
                    novo_pedido = self.pedidos_por_adicionar.pop()
                    if novo_pedido.is_prioritario():
                         self.pedidos_por_responder["prioritários"].append(novo_pedido)
                    else:
                         self.pedidos_por_responder["normais"].append(novo_pedido)


     # Imprime as estatísticas no final da simulação
     def calcular_estatisticas(self):
          print("Eficiência da simulação:")
          print(f"Nº de pedidos cumpridos = {self.pedidos_respondidos}")
          print(f"Tempo médio de resposta = {self.tempo_resposta_total/self.pedidos_respondidos}")
          print(f"Nº de pedidos rejeitados = {self.pedidos_rejeitados}")
          print(f"Custos operacionais totais = {self.custos_operacionais_total}")
          print(f"Emissões de CO2 estimadas = {self.emissoes_total}")
          print(f"Quilómetros percorridos sem passageiros = {self.km_sem_passageiros}")

     
     # Usa o algoritmo da simulação para calcular o caminho entre dois pontos
     def usar_algoritmo(self, origem, destino):
          match self.algoritmo:
               case 1:
                    return BFS(self.cidade,origem,destino)
               case 2:
                    return DFS(self.cidade,origem,destino,[],set())
               case 3:
                    return aStar(self.cidade,origem,destino)
               case 4: 
                    return greedy(self.cidade,origem,destino)
               case _:
                    return None


     # Responde ao pedido recebido, se possível 
     def responde_pedido(self, pedido: Pedido):
          veiculo_escolhido = None
          melhor_tempo = None
          if pedido.getPreferenciaAmbiental():
               for ve in self.veiculos_disponiveis.values():
                    if ve.getTipo == "Elétrico": ### ainda há outros fatores a considerar
                         resposta = self.usar_algoritmo(ve.getLocalizacao(),pedido.getOrigem())
                         tempo_resposta = self.cidade.calcular_distancia(resposta) ### dps alterar pra calcular tempo em vez de distancia
                         if melhor_tempo == None or melhor_tempo > tempo_resposta:
                              melhor_tempo = tempo_resposta
                              veiculo_escolhido = ve
          
          else:
               pass # fazer dps

          if pedido.getTempoEsperaMax >= melhor_tempo:
               veiculo_escolhido = self.veiculos_disponiveis.pop(veiculo_escolhido.getID())
               caminho = resposta = self.usar_algoritmo(pedido.getOrigem(),pedido.getDestino()) 
               veiculo_escolhido.setTempoAteDisponivel(melhor_tempo + self.cidade.calcular_distancia(caminho))
               self.veiculos_ocupados[veiculo_escolhido.getID()] = veiculo_escolhido
               
               self.pedidos_respondidos += 1
               self.tempo_resposta_total += melhor_tempo
               ## resto das esttaisticas

          else: 
               pass ### por acabar
               

     # Seleciona o próximo pedido a ser respondido 
     def gestor_pedidos(self, fim: Event):
          while not fim.is_set:
               prox_pedido = None
               if len(self.pedidos_por_responder["prioritários"] > 0):
                    prox_pedido = self.pedidos_por_responder["prioritários"].pop(0)
               elif len(self.pedidos_por_responder["normais"] > 0):
                    prox_pedido = self.pedidos_por_responder["normais"].pop(0)

               if prox_pedido:
                    self.responde_pedido(prox_pedido)    


     # Corre a simulação
     def run(self):
          match self.algoritmo: ## ver se esta é a melhor estrategia dps
               case 1:
                    a = "BFS (Pesquisa em Largura)"
               case 2:
                    a = "DFS (Pesquisa em Profundidade)"
               case 3:
                    a = "A*"
               case 4: 
                    a = "Greedy (Pesquisa gulosa)"
          print("A iniciar simulação usando o algoritmo " + a) # pôr mais info depois
          
          fim = Event()
          Thread(target = self.gestor_pedidos, args=(fim)).start()
          
          while self.tempo != Hora(5,59):
               self.adicionaPedidos()
               self.tempo.incrementaMinuto()

          fim.set() ### termina a execução da thread que lidava com os pedidos
          
          self.calcular_estatisticas()