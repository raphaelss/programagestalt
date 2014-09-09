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
