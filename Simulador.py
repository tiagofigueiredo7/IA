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
     def __init__(self, veiculos: list, pedidos: list, hora_inicial: Hora, cidade: Cidade, algoritmo: int, modo: int):
          self.veiculos = veiculos
          self.pedidos_por_adicionar = pedidos
          self.pedidos_por_responder = {"prioritários": [], "normais": []}
          self.tempo = hora_inicial
          self.cidade = cidade
          self.algoritmo = algoritmo
          self.modo = modo

          ## estatísticas
          self.pedidos_respondidos = 0
          self.pedidos_rejeitados = [0,0,0] # total, prioritarios, hora de ponta
          self.tempo_resposta = 0
          self.emissoes = 0
          self.custos = 0
          self.km_sem_passageiros = 0
          self.partilha_boleia = 0
          self.ambiental_eletrico = 0 ## pedidos ambientais respeitados
          self.pedidos_ambientais = 0
          for p in self.pedidos_por_adicionar:
               if p.getPreferenciaAmbiental():
                    self.pedidos_ambientais += 1


     # Adiciona entre pedidos ao sistema
     def adicionaPedidos(self):
          if self.tempo.eHoraPonta():
               num_pedidos = random.randint(1,4)
          else:
               num_pedidos = random.randint(0,1) ## horas mais mortas

          while len(self.pedidos_por_adicionar) > 0 and num_pedidos > 0:
               num_pedidos = num_pedidos - 1
               novo_pedido = self.pedidos_por_adicionar.pop()
               queue = self.pedidos_por_responder["prioritários"] if novo_pedido.getPrioridade() else self.pedidos_por_responder["normais"]
               i = 0
               while i < len(queue) and queue[i].getTempoEsperaMax() <= novo_pedido.getTempoEsperaMax():
                    i += 1

               queue.insert(i, novo_pedido)


     # Imprime as estatísticas no final da simulação
     def calcular_estatisticas(self):
          print(f"Taxa de sucesso: {round((self.pedidos_respondidos*100/(self.pedidos_respondidos+self.pedidos_rejeitados[0])),1)}%")
          print(f"Nº de pedidos cumpridos: {self.pedidos_respondidos}")
          print(f"Nº de pedidos rejeitados: {self.pedidos_rejeitados[0]}")
          print(f"- {self.pedidos_rejeitados[1]} prioritários")
          print(f"- {self.pedidos_rejeitados[2]} em hora de ponta")
          if self.pedidos_respondidos > 0:
               print(f"Tempo médio de resposta: {round((self.tempo_resposta/self.pedidos_respondidos),2)} minutos")
          print(f"Pedidos com preferência ambiental respeitados: {round(self.ambiental_eletrico*100/self.pedidos_ambientais,1)}%")
          print(f"Boleias partilhadas: {self.partilha_boleia}")
          print(f"Custos operacionais: {round(self.custos,2)}€")
          print(f"Emissões de CO2: {round(self.emissoes/1000,1)}kg")
          print(f"Distância percorrida sem passageiros: {self.km_sem_passageiros}km")


     # Algoritmo usado na simulação calcula o caminho entre dois pontos
     def usar_algoritmo(self, o, d):
          # primeiro verifica a cache
          if d not in self.cidade.cache[o].keys():
               match self.algoritmo:
                    case 1:
                         return BFS(self.cidade,o,d)
                    case 2:
                         return DFS(self.cidade,o,d,[],set())
                    case 3:
                         return aStar(self.cidade,o,d,self.tempo)
                    case _:
                         return greedy(self.cidade,o,d,self.tempo)
          else:
               return (self.cidade.cache[o]).get(d)


     # Verifica se o carro tem as condições necessárias para responder ao pedido
     # Se sim, devolve um tuplo: (km's até origem, minutos até origem, km's até destino, minutos até destino)
     # Para evitar ter que recalcular estes valores
     def capaz_de_responder(self, carro: Carro, pedido: Pedido):
          if pedido.getNumPassageiros() <= carro.getCapacidadePassageiros() + carro.getNrPassageiros():
               path1 = self.usar_algoritmo(carro.getLocalizacao(),pedido.getOrigem()).copy()
               path1.pop()
               path2 = self.usar_algoritmo(pedido.getOrigem(),pedido.getDestino())
               t1 = carro.naRota(path1+path2) 
               if t1 in range(pedido.getTempoEsperaMax()): ## se conseguir dar boleia a tempo
                    self.partilha_boleia += 1
                    return 0,[t1],0,0,None # não são gastos recursos extra!   
               d1, t1 = self.cidade.calcular_distancia_tempo(path1,self.tempo,0)
               if carro.getTempoAteDisponivel() + sum(t1) <= pedido.getTempoEsperaMax():
                    d2,t2 = self.cidade.calcular_distancia_tempo(path2,self.tempo,0)
                    if d1+d2+20 <= carro.getAutonomiaAtual(): # evitar que carro fique "na reserva"
                         return d1,t1,d2,t2,path1+path2

          return None,None,None,None,None


     # Envia carro escolhido para cumprir pedido
     def envia_carro(self, c: Carro, r):
          self.pedidos_respondidos += 1
          if r[4]: ### se não for boleia partilhada
               d = r[0] + r[2]
               c.setAutonomiaAtual(c.getAutonomiaAtual() - d)
               self.emissoes += (c.getImpactoAmbiental() * d)
               self.custos += (c.getCustoKM() * d)
               self.km_sem_passageiros += r[0]
               c.setRota(r[4],r[1]+r[3]) ### muda rota e e tempo até estar disponivel
               self.tempo_resposta += sum(r[1])
               if c.getAutonomiaAtual() < 50:
                    self.abastecer(c)
          self.tempo_resposta += sum(r[1])


     # Procura um carro para responder ao pedido, se possível
     def responde_pedido(self, pedido: Pedido):
          veiculo_escolhido = None
          r = None
          frota = self.veiculos.copy()  # veículos elétricos estão primeiro na lista
          if not pedido.preferenciaAmbiental:
               frota.reverse() # pedidos não ambientais começam a procurar pelos de combustão
         
          match self.modo:
               case 1:   ### modo básico - envia o primeiro veículo que encontra
                    for ve in frota:
                         d1,t1,d2,t2,path = self.capaz_de_responder(ve,pedido)
                         if t1 != None:
                              veiculo_escolhido = ve 
                              r = (d1,t1,d2,t2,path)
                              break
               case 2:   ### modo rápido - envia o veículo mais rápido a responder
                    for ve in frota:
                         d1,t1,d2,t2,path = self.capaz_de_responder(ve,pedido)
                         if (t1 != None and (r == None or sum(r[1]) > sum(t1))):
                              r = (d1,t1,d2,t2,path)
                              veiculo_escolhido = ve
               case 3:   ### modo económico - envia o veículo mais barato
                    d = 0
                    for ve in frota:
                         d1,t1,d2,t2,path = self.capaz_de_responder(ve,pedido)
                         if t1 != None and (r == None or d > ve.getCustoKM()*(d1+d2)):
                              d = ve.getCustoKM()*(d1+d2)
                              r = (d1,t1,d2,t2,path)
                              veiculo_escolhido = ve
               case _:   ### modo ambiental - envia o veículo menos poluente
                    e = 0
                    for ve in frota:
                         d1,t1,d2,t2,path = self.capaz_de_responder(ve,pedido)
                         if t1 != None and (r == None or e > ve.getImpactoAmbiental()*(d1+d2)):
                              e = ve.getImpactoAmbiental()*(d1+d2)
                              r = (d1,t1,d2,t2,path)
                              veiculo_escolhido = ve

          if veiculo_escolhido:
               veiculo_escolhido.incNrPassageiros(pedido.getNumPassageiros())
               self.envia_carro(veiculo_escolhido,r)
               if pedido.preferenciaAmbiental and veiculo_escolhido.getTipo()=="Eletrico":
                    self.ambiental_eletrico += 1
          else:
               self.pedidos_rejeitados[0] += 1
               if pedido.getPrioridade():
                    self.pedidos_rejeitados[1] += 1
               if self.tempo.eHoraPonta():
                    self.pedidos_rejeitados[2] += 1
          

     # Procura ponto de abastecimento/estação de carregamento para carro reabastecer
     def abastecer(self, carro:Carro):
          tipo = tl.Estacao_Carregamento if carro.getTipo() == "Eletrico" else tl.Posto_Combustivel
          if tipo not in self.cidade.cache[carro.getLocalizacao()].keys():
               match self.algoritmo:
                    case 1:
                         path = BFS_tipo(self.cidade,carro.getLocalizacao(),tipo)
                    case 2:
                         path = DFS_tipo(self.cidade,carro.getLocalizacao(),tipo,[],set())
                    case 3:
                         path = aStar_tipo(self.cidade,carro.getLocalizacao(),tipo, carro.getAutonomiaAtual(),self.tempo)
                    case _:
                         path = greedy_tipo(self.cidade,carro.getLocalizacao(),tipo,self.tempo)
          else:
               path = (self.cidade.cache[carro.getLocalizacao()]).get(tipo)

          if path:
               d,t = self.cidade.calcular_distancia_tempo(path,self.tempo,carro.getTempoReabastecimento())
               if d > carro.getAutonomiaAtual():
                    print(f"Carro {carro.getID()} desativado.")
                    self.veiculos.remove(carro) # carro passa a ser inútil
               else:
                    carro.reabastecer()
                    carro.incRota(path,t)
                    self.emissoes += (carro.getImpactoAmbiental() * d)
                    self.custos += (carro.getCustoKM() * d)
                    self.km_sem_passageiros += d

          else: # em principio, é impossivel acontecer
               print(f"Não foram encontrados postos de abastecimento. Carro {carro.getID()} desativado.")
               self.veiculos.remove(carro)


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
          for v in self.veiculos:
               v.decTempoAteDisponivel()
          for f in self.pedidos_por_responder.values():
               i = 0
               for p in f:
                    if not p.decTempoEsperaMax():
                         f.pop(i)
                         self.pedidos_rejeitados[0] += 1
                         if p.getPrioridade():
                              self.pedidos_rejeitados[1] += 1
                         if self.tempo.eHoraPonta():
                              self.pedidos_rejeitados[2] += 1
                         print("Pedido não foi respondido a tempo.")
                    i+=1


     # Corre a simulação
     def run(self):
          match self.algoritmo:
               case 1:
                    a = "de Pesquisa em Largura (BFS)"
               case 2:
                    a = "de Pesquisa em Profundidade (DFS)"
               case 3:
                    a = "A*"
               case 4:
                    a = "de Pesquisa Gulosa (Greedy)"
          print("\nA iniciar simulação usando o algoritmo " + a + "...")
          fim = Event()
          Thread(target = self.gestor_pedidos, args=(fim,)).start()

          while len(self.pedidos_por_adicionar) > 0:
               self.adicionaPedidos()
               time.sleep(0.01)
               self.passaMinuto()

          fim.set()     # termina a execução da thread que lidava com os pedidos
          print(f"Simulação terminada às {self.tempo}h\n")
          time.sleep(2)
          self.calcular_estatisticas()