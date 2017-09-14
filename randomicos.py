import random
from gestalt import altura_maxima,altura_minima,duracoes_possiveis
from lilypond import quialteras_n

duracoes_sem_quialtera = list(set(duracoes_possiveis) - set(quialteras_n))

class Aleatorio:
    def __init__(self, quantidade):
        self.quantidade = quantidade

    def gerar_altura(self):
        elementos = []
        for i in range(self.quantidade):
            elementos.append(random.randint(altura_minima, altura_maxima))
        return elementos

    def gerar_duracao(self):
        elementos = []
        contador = 0
        quialtera = False
        dur_atual = 0
        while contador < self.quantidade:
            if dur_atual % 60 == 0:
                duracao_randomica = duracoes_possiveis[random.randint(0, 22)]
            else:
                duracao_randomica = duracoes_sem_quialtera[random.randint(0,len(duracoes_sem_quialtera)-1)]
            if duracao_randomica in quialteras_n:
                quialtera = True
                n = quialteras_n[duracao_randomica]
            else:
                n = 1
            if (contador + n) > self.quantidade :
                continue
            dur_atual = duracao_randomica * n + dur_atual
            contador = contador + n
            while n > 0:
                elementos.append(duracao_randomica)
                n = n - 1
        return elementos
