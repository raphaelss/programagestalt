from lilypond import gerar_lilypond
import randomicos
import sys
import os.path
import arquivo

altura_minima = 48
altura_maxima = 60
duracoes_possiveis = [10,12,15,20,24,30,40,45,48,60,75,80,90,105,120,135,150,165,180,195,210,225,240]
niveis_default = "cqgs"

class Nivel:
    def __init__(self, alturas, duracoes, picos_anterior = False):
        self.altura = alturas
        self.duracao = duracoes
        self.intervalo = []
        i = 1
        while i < len(self.altura):
            self.intervalo.append(10 * abs(self.altura[i] - self.altura[i-1]))
            i = i+1
        self.distancia = []
        self.disjuncao = []
        for j in range(len(self.intervalo)):
            self.distancia.append(self.duracao[j] + self.intervalo[j])
            if picos_anterior:
                self.disjuncao.append(self.distancia[j] + picos_anterior[j])
            else:
                self.disjuncao.append(self.distancia[j])

    def __repr__(self):
        return "Altura = {0}\nIntervalo = {1}\nDuração = {2}\nDistância = {3}\nDisjunção = {4}".format(self.altura,
                                                                                                       self.intervalo,
                                                                                                       self.duracao,
                                                                                                       self.distancia,
                                                                                                       self.disjuncao)

class Evento:
    def __init__(self, altura, duracao, nr_niveis):
        self.altura = altura
        self.duracao = duracao
        self.niveis = [False] * nr_niveis

    def __repr__(self):
        return "\nAltura = {0}\nDuração = {1}\nNíveis = {2}".format(self.altura,
                                                                  self.duracao,
                                                                  self.niveis)

def calcular_eventos(alturas, duracoes, niveis):
    eventos = []
    cur = 0
    i_cur_niveis = [(0, 0)] * len(niveis)
    for i in range(len(alturas)):
        ev = Evento(alturas[i], duracoes[i], len(niveis))
        for j in range(len(niveis)):
            i_nivel, cur_nivel = i_cur_niveis[j]
            if cur == cur_nivel:
                ev.niveis[j] = i_nivel + 1
                i_cur_niveis[j] = (i_nivel + 1, cur_nivel + niveis[j].duracao[i_nivel])
        eventos.append(ev)
        cur = cur + ev.duracao
    return eventos

def achar_picos(lista):
    indices = []
    valores = []
    for i in range(1, len(lista)-1):
        if lista[i] > lista[i-1] and lista[i] > lista[i+1]:
            valores.append(lista[i])
            indices.append(i)
    return (indices, valores)

def media(lista):
    return sum(lista)/len(lista)

def novo_nivel(anterior):
    picos_indice, picos_valor = achar_picos(anterior.disjuncao)
    alturas = []
    duracoes = []
    inicio = 0
    for i in picos_indice:
        fim = i+1
        alturas.append(media(anterior.altura[inicio:fim]))
        duracoes.append(sum(anterior.duracao[inicio:fim]))
        inicio = fim
    alturas.append(media(anterior.altura[inicio:len(anterior.altura)]))
    duracoes.append(sum(anterior.duracao[inicio:len(anterior.duracao)]))
    return Nivel(alturas, duracoes, picos_valor)

def gerar(arquivo, obj, niveis_spec = niveis_default):
    alturas = obj.gerar_altura()
    duracoes = obj.gerar_duracao()
    niveis = [novo_nivel(Nivel(alturas, duracoes))]
    for i in range(len(niveis_spec) - 1):
        niveis.append(novo_nivel(niveis[i]))
    eventos = calcular_eventos(alturas, duracoes, niveis)
    gerar_lilypond(arquivo, eventos, niveis_spec)

if __name__ == '__main__':
    if os.path.isfile(sys.argv[1]):
        obj = arquivo.abrir(sys.argv[1])
    else:
        obj = randomicos.Aleatorio(int(sys.argv[1]))
    gerar(sys.argv[2], obj)
