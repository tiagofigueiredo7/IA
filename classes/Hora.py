
class Hora:
     def __init__(self, hora, minuto):
          self.hora = hora
          self.minuto = minuto

     def getHora(self):
          return self.hora

     def getMinuto(self):
          return self.minuto

     def incrementaMinuto(self):
          self.minuto += 1
          if self.minuto >= 60:
               self.minuto = 0
               self.hora += 1
               if self.hora >= 24:
                    self.hora = 0

     def __str__(self):
          return f"{self.hora:02}:{self.minuto:02}"
     
     def ehHoraPonta(self):
          ## Define horas de ponta como 7:00-9:00 e 17:00-19:00
          if (self.hora >= 7 and self.hora < 9) or (self.hora >= 17 and self.hora < 19):
               return True
          return False