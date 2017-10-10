import csv
import re

class Arquivo:
    def __init__(self, path):
        rp = re.compile("^ *(\d+) +(\d+)\n?$")
        self.alturas = []
        self.duracoes = []
        linecount = 1
        with open(path) as f:
            for line in f:
                match = rp.match(line)
                if match:
                    self.alturas.append(int(match.group(1)))
                    self.duracoes.append(int(match.group(2)))
                else:
                    print("Erro na linha", linecount, ":", line)
                    exit()
                linecount = linecount + 1

    def gerar_altura(self):
        return self.alturas

    def gerar_duracao(self):
        return self.duracoes

class Csv:
    def __init__(self, path):
        self.alturas = []
        self.duracoes = []
        with open(path) as f:
            for row in csv.reader(f, delimiter=';'):
                self.alturas.append(int(row[3]))
                self.duracoes.append(round(float(row[1].replace(',','.')) * 60))

    def gerar_altura(self):
        return self.alturas

    def gerar_duracao(self):
        return self.duracoes

def abrir(path):
    if path.endswith('csv'):
        return Csv(path)
    else:
        return Arquivo(path)
