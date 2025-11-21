from classes.Hora import Hora
from parsers import parser
from GestorFrota import GestorFrota
from GestorPedidos import GestorPedidos
from Simulador import Simulador

def main():
     
     ## parse de dados

     carros, pedidos = parser( "data/Carros.csv", "data/Pedidos.csv")

     tempo = Hora(6,0)

     gestor_frota = GestorFrota(carros)
     gestor_pedidos = GestorPedidos()

     while True:##not simulador.terminou():
          # Atualiza pedidos dinâmicos
          gestor_pedidos.adicionaPedidos(pedidos)
          
          # Executa lógica principal de alocação de veículos
           ##simulador.executa_ciclo()

          # Avança o tempo
          tempo = tempo.incrementaMinuto()       

          break


     ## calcula métricas
     ## temos de guardar os tempos, consumos e assim .....

if __name__ == "__main__":
    main()