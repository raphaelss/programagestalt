import random
from gestalt import altura_maxima,altura_minima,duracoes_possiveis
from lilypond import quialteras

class AlturaAleatorio:
    def gerar_altura(self, quantidade):
        elementos = []
        for i in range(quantidade):
            elementos.append(random.randint(altura_minima, altura_maxima))
        return elementos

class DuracaoAleatorio:
    def gerar_duracao(self, quantidade):
        elementos = []
        duracoes_sem_quialtera = list(set(duracoes_possiveis) - set(quialteras))
        contador = 0
        quialtera = False
        dur_atual = 0
        while contador < quantidade:
            if dur_atual % 60 == 0:
                duracao_randomica = duracoes_possiveis[random.randint(0, 22)]
            else:
                duracao_randomica = duracoes_sem_quialtera[random.randint(0,len(duracoes_sem_quialtera)-1)]
            if duracao_randomica==10:
                quialtera = True
                n = 6
            elif duracao_randomica==12:
                quialtera = True
                n = 5
            elif duracao_randomica==20:
                quialtera = True
                n = 3
            elif duracao_randomica==24:
                quialtera = True
                n = 5
            elif duracao_randomica==40:
                quialtera = True
                n = 3
            elif duracao_randomica==48:
                quialtera = True
                n = 5
            elif duracao_randomica==80:
                quialtera = True
                n = 3
            else:
                n = 1
            if (contador + n) > quantidade :
                continue
            dur_atual = duracao_randomica * n + dur_atual
            contador = contador + n
            while n > 0:
                elementos.append(duracao_randomica)
                n = n - 1
        return elementos