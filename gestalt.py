from lilypond import gerar_lilypond
import randomicos
import sys
import os.path
import arquivo

altura_minima = 48
altura_maxima = 60
duracoes_possiveis = [10,12,15,20,24,30,40,45,48,60,75,80,90,105,120,135,150,165,180,195,210,225,240]

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
    def __init__(self, altura, duracao):
        self.altura = altura
        self.duracao = duracao
        self.clang = False
        self.sequencia = False
        self.segmento = False
        self.secao = False

def calcular_eventos(alturas, duracoes, clang, sequencia, segmento, secao):
    eventos = []
    cur = 0
    i_clang = 0
    i_sequencia = 0
    i_segmento = 0
    i_secao = 0
    cur_clang = 0
    cur_sequencia = 0
    cur_segmento = 0
    cur_secao = 0
    ev = Evento(alturas[0],duracoes[0])
    for i in range(len(alturas)):
        ev = Evento(alturas[i],duracoes[i])
        if cur == cur_clang:
            ev.clang = i_clang+1
            cur_clang += clang.duracao[i_clang]
            i_clang += 1
        if cur == cur_sequencia:
            ev.sequencia = i_sequencia+1
            cur_sequencia += sequencia.duracao[i_sequencia]
            i_sequencia += 1
        if cur == cur_segmento:
            ev.segmento = i_segmento+1
            cur_segmento += segmento.duracao[i_segmento]
            i_segmento += 1
        if cur == cur_secao:
            ev.secao = i_secao+1
            cur_secao += secao.duracao[i_secao]
            i_secao += 1
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

def gerar(arquivo, alturas, duracoes):
    elemento = Nivel(alturas, duracoes)
    clang = novo_nivel(elemento)
    sequencia = novo_nivel(clang)
    segmento = novo_nivel(sequencia)
    secao = novo_nivel(segmento)
    eventos = calcular_eventos(alturas, duracoes, clang, sequencia, segmento, secao)
    gerar_lilypond(arquivo, eventos)

if __name__ == '__main__':
    if os.path.isfile(sys.argv[1]):
        arq = arquivo.Arquivo(sys.argv[1])
        alturas = arq.gerar_altura()
        duracoes = arq.gerar_duracao()
    else:
        quant = int(sys.argv[1])
        alturas = randomicos.AlturaAleatorio().gerar_altura(quant)
        duracoes = randomicos.DuracaoAleatorio().gerar_duracao(quant)
    arquivo_saida = sys.argv[2]
    gerar(arquivo_saida, alturas, duracoes)
