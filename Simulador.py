from threading import Thread, Event
import time
from classes.Carro import Carro
from classes.Cidade import Cidade
from classes.Hora import Hora
from classes.Pedido import Pedido
from classes.Tipo_Localizacao import Tipo_Localizacao as tl
from algoritmos import BFS, DFS, greedy, aStar, BFS_tipo, DFS_tipo, aStar_tipo, greedy_tipo
import random

class Simulador:
     def __init__(self, veiculos, pedidos, hora_inicial: Hora, cidade: Cidade, algoritmo):
          self.veiculos = veiculos
          self.pedidos_por_adicionar = pedidos
          self.pedidos_por_responder = {"prioritários": [], "normais": []}
          self.tempo = hora_inicial
          self.cidade = cidade
          self.algoritmo = algoritmo

          ## estatísticas
          self.pedidos_respondidos = 0
          self.pedidos_rejeitados = 0
          self.tempo_resposta_total = 0
          self.emissoes = 0
          self.custos = 0
          self.km_sem_passageiros = 0
          ### como fazer taxa de ocupação da frota??
          self.type_error = 0
          self.time_error = 0
          self.distance_error = 0
          self.cap_error = 0


     # Adiciona entre 0 a 2 pedidos ao sistema
     def adicionaPedidos(self):
          num_pedidos = random.randint(0,2)
          while len(self.pedidos_por_adicionar) > 0 and num_pedidos > 0:
               num_pedidos = num_pedidos - 1
               novo_pedido = self.pedidos_por_adicionar.pop()
               if novo_pedido.getPrioridade():
                    self.pedidos_por_responder["prioritários"].append(novo_pedido)
               else:
                    self.pedidos_por_responder["normais"].append(novo_pedido)


     # Imprime as estatísticas no final da simulação
     def calcular_estatisticas(self):
          print(f"Taxa de sucesso = {round((self.pedidos_respondidos*100)/(self.pedidos_respondidos+self.pedidos_rejeitados),1)}%")
          print(f"Nº de pedidos cumpridos = {self.pedidos_respondidos}")
          if self.pedidos_respondidos > 0:
               print(f"Tempo médio de resposta = {round((self.tempo_resposta_total/self.pedidos_respondidos),2)} minutos")
          print(f"Nº de pedidos rejeitados = {self.pedidos_rejeitados}")
          print(f"Custos operacionais = {self.custos}€")
          print(f"Emissões de CO2 = {self.emissoes}g")
          print(f"Distância percorrida sem passageiros = {self.km_sem_passageiros}km")

          total_errors = self.type_error + self.time_error + self.distance_error + self.cap_error
          print("\nCausas dos pedidos recusados:\n")
          print(f"\tTempo de espera: {round((self.time_error*100)/total_errors,1)}%")
          print(f"\tPreferência ambiental: {round((self.type_error*100)/total_errors,1)}%")
          print(f"\tCapacidade para nº de passageiros: {round((self.cap_error*100)/total_errors,1)}%")
          print(f"\tDistância elevada: {round((self.distance_error*100)/total_errors,1)}%")


     # Algoritmo usado na simulação calcula o caminho entre dois pontos
     def usar_algoritmo(self, o, d):
          match self.algoritmo:
               case 1:
                    return BFS(self.cidade,o,d)
               case 2:
                    return DFS(self.cidade,o,d,[],set())
               case 3:
                    return aStar(self.cidade,o,d)
               case _:
                    return greedy(self.cidade,o,d)


     # Verifica se o carro tem as condições necessárias para responder ao pedido
     # Se sim, devolve um tuplo: (km's até origem, minutos até origem, km's até destino, minutos até destino)
     # Para evitar ter que recalcular estes valores
     def capaz_de_responder(self, carro: Carro, pedido: Pedido):
          tipo_valido = (carro.getTipo == "Elétrico") if pedido.getPreferenciaAmbiental() else True
          if tipo_valido:
               if pedido.getNumPassageiros() <= carro.getCapacidadePassageiros():
                    path1 = self.usar_algoritmo(carro.getLocalizacao(),pedido.getOrigem())
                    d1, t1 = self.cidade.calcular_distancia_tempo(path1)
                    if carro.getTempoAteDisponivel() + t1 <= pedido.getTempoEsperaMax():
                         path2 = self.usar_algoritmo(pedido.getOrigem(),pedido.getDestino())
                         d2,t2 = self.cidade.calcular_distancia_tempo(path2)
                         if d1+d2+20 <= carro.getAutonomiaAtual(): # evitar que carro fique "na reserva"
                              return d1,t1,d2,t2
                         else:
                              self.distance_error += 1
                    else:
                         self.time_error += 1 
               else:
                    self.cap_error += 1
          else:
               self.type_error +=1

          return None,None,None,None

     #### QUE VERSÃO USAR???
     # Responde ao pedido, se possível (Versão que envia o carro mais rápido possível)
     def responde_pedido_urgente(self, pedido: Pedido):
          veiculo_escolhido = None
          melhor_resposta = None

          for ve in self.veiculos.values():
               d1,t1,d2,t2 = self.capaz_de_responder(ve,pedido)
               if t1 and (melhor_resposta == None or melhor_resposta[1] > t1):
                    melhor_resposta = (d1,t1,d2,t2)
                    veiculo_escolhido = ve

          if veiculo_escolhido == None:
               self.pedidos_rejeitados += 1

          else:
               d = melhor_resposta[0] + melhor_resposta[2]
               veiculo_escolhido.setAutonomiaAtual(veiculo_escolhido.getAutonomiaAtual() - d)
               veiculo_escolhido.setTempoAteDisponivel(melhor_resposta[1] + melhor_resposta[3])
               veiculo_escolhido.setLocalizacao(pedido.getDestino())

               self.pedidos_respondidos += 1
               self.tempo_resposta_total += melhor_resposta[1]
               self.emissoes += (veiculo_escolhido.getImpactoAmbiental() * d)
               self.custos += (veiculo_escolhido.getCustoKM() * d)
               self.km_sem_passageiros += melhor_resposta[0]

               if veiculo_escolhido.getAutonomiaAtual() < 50:
                    self.abastecer(veiculo_escolhido)


     # Responde ao pedido, se possível (Versão que envia o primeiro carro disponível)
     def responde_pedido(self, pedido: Pedido):
          for ve in self.veiculos.values():
               d1,t1,d2,t2 = self.capaz_de_responder(ve,pedido)
               if t1:
                    d = d1 + d2
                    ve.setAutonomiaAtual(ve.getAutonomiaAtual() - d)
                    ve.setTempoAteDisponivel(t1 + t2)
                    ve.setLocalizacao(pedido.getDestino())

                    self.pedidos_respondidos += 1
                    self.tempo_resposta_total += t1
                    self.emissoes += (ve.getImpactoAmbiental() * d)
                    self.custos += (ve.getCustoKM() * d)
                    self.km_sem_passageiros += d1

                    if ve.getAutonomiaAtual() < 50:
                         self.abastecer(ve)
                    return 
          
          self.pedidos_rejeitados += 1
          

     # Procura ponto de abastecimento/estação de carregamento para carro reabastecer
     def abastecer(self, carro:Carro):
          tipo = tl.Estacao_Carregamento if carro.getTipo == "Elétrico" else tl.Posto_Combustivel
          match self.algoritmo:
               case 1:
                    path = BFS_tipo(self.cidade,carro.getLocalizacao(),tipo)
               case 2:
                    path = DFS_tipo(self.cidade,carro.getLocalizacao(),tipo,[],set())
               case 3:
                    path = aStar_tipo(self.cidade,carro.getLocalizacao(),tipo, carro.getAutonomiaAtual())
               case _:
                    path = greedy_tipo(self.cidade,carro.getLocalizacao(),tipo)

          if path:
               d,t = self.cidade.calcular_distancia_tempo(path)
               if d > carro.getAutonomiaAtual():
                    print(f"Não foram encontrados postos de abastecimento a uma distância alcançável. Carro {carro.getID()} desativado.")
                    self.veiculos.pop(carro.getID()) # carro passa a ser inútil
               else:
                    carro.reabastecer()
                    carro.setTempoAteDisponivel(carro.getTempoAteDisponivel() + t + carro.getTempoReabastecimento())
                    carro.setLocalizacao(path[-1])
                    self.emissoes += (carro.getImpactoAmbiental() * d)
                    self.custos += (carro.getCustoKM() * d)
                    self.km_sem_passageiros += d

          else: # em principio, é impossivel de acontecer
               print(f"Não foram encontrados postos de abastecimento. Carro {carro.getID()} desativado.")
               self.veiculos.pop(carro.getID())


     # Seleciona o próximo pedido a ser respondido
     def gestor_pedidos(self, fim: Event):
          while not fim.is_set():
               prox_pedido = None
               if len(self.pedidos_por_responder["prioritários"]) > 0:
                    prox_pedido = self.pedidos_por_responder["prioritários"].pop(0)
               elif len(self.pedidos_por_responder["normais"]) > 0:
                    prox_pedido = self.pedidos_por_responder["normais"].pop(0)

               if prox_pedido:
                    self.responde_pedido(prox_pedido)


     # Simula a passagem de um minuto
     def passaMinuto(self):
          self.tempo.incrementaMinuto()
          for v in self.veiculos.values():
               if v.getTempoAteDisponivel() > 0:
                    v.decTempoAteDisponivel()
          for f in self.pedidos_por_responder.values():
               index = 0
               for p in f:
                    if not p.decTempoEsperaMax():
                         f.pop(index)
                         self.pedidos_rejeitados += 1
                         print("Pedido não foi respondido a tempo.")
                    index+=1


     # Corre a simulação
     def run(self):
          match self.algoritmo:
               case 1:
                    a = "de Pesquisa em Largura"
               case 2:
                    a = "e Pesquisa em Profundidade"
               case 3:
                    a = "A*"
               case 4:
                    a = "de Pesquisa Gulosa (Greedy)"
          print("\nA iniciar simulação usando o algoritmo " + a + "...\n")
          fim = Event()
          Thread(target = self.gestor_pedidos, args=(fim,)).start()

          while str(self.tempo) != "22:00" and len(self.pedidos_por_adicionar) > 0:
               self.adicionaPedidos()
               time.sleep(0.01)
               self.passaMinuto()

          time.sleep(1) # dar um segundo para o gestor poder responder aos ultimos pedidos
          fim.set()     # termina a execução da thread que lidava com os pedidos
          self.calcular_estatisticas()