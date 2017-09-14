pitch_names = {0: 'c',
               1: 'des',
               2: 'd',
               3: 'ees',
               4:'e',
               5:'f',
               6:'ges',
               7:'g',
               8:'aes',
               9:'a',
               10:'bes',
               11:'b'}

duracoes_string = {10:"\\times 4/6 {{ {cor[0]}{0}16[{mp[0]} {cor[1]}{1}16{mp[1]} {cor[2]}{2}16{mp[2]} {cor[3]}{3}16{mp[3]} {cor[4]}{4}16{mp[4]} {cor[5]}{5}16]{mp[5]} }}",
                   12:"\\times 4/5 {{ {cor[0]}{0}16[{mp[0]} {cor[1]}{1}16{mp[1]} {cor[2]}{2}16{mp[2]} {cor[3]}{3}16{mp[3]} {cor[4]}{4}16]{mp[4]} }}",
                   15:"{cor}{0}16{mp}",
                   20:"\\times 2/3 {{ {cor[0]}{0}8[{mp[0]} {cor[1]}{1}8{mp[1]} {cor[2]}{2}8]{mp[2]} }}",
                   24:"\\times 4/5 {{ {cor[0]}{0}8[{mp[0]} {cor[1]}{1}8{mp[1]} {cor[2]}{2}8{mp[2]} {cor[3]}{3}8{mp[3]} {cor[4]}{4}8]{mp[4]} }}",
                   30:"{cor}{0}8{mp}",
                   40:"\\times 2/3 {{ {cor[0]}{0}4{mp[0]} {cor[1]}{1}4{mp[1]} {cor[2]}{2}4{mp[2]} }}",
                   45:"{cor}{0}8.{mp}",
                   48:"\\times 4/5 {{ {cor[0]}{0}4{mp[0]} {cor[1]}{1}4{mp[1]} {cor[2]}{2}4{mp[2]} {cor[3]}{3}4{mp[3]} {cor[4]}{4}4{mp[4]} }}",
                   60:"{cor}{0}4{mp}",
                   75:"{cor}{0}4~ {0}16",
                   80:"\\times 2/3 {{ {cor[0]}{0}2{mp[0]} {cor[1]}{1}2{mp[1]} {cor[2]}{2}2{mp[2]} }}",
                   90:"{cor}{0}4.{mp}",
                   105:"{cor}{0}4~{mp} {0}8.",
                   120:"{cor}{0}2{mp}",
                   135:"{cor}{0}2~{mp} {0}16",
                   150:"{cor}{0}2~{mp} {0}8",
                   165:"{cor}{0}2~{mp} {0}8.",
                   180:"{cor}{0}2.{mp}",
                   195:"{cor}{0}2.~{mp} {0}16",
                   210:"{cor}{0}2.~{mp} {0}8",
                   225:"{cor}{0}2.~{mp} {0}8.",
                   240:"{cor}{0}1{mp}"}

quialteras_n = {10:6, 12:5, 20:3, 24:5, 40:3, 48:5, 80:3}

red = "\\once \\override NoteHead #'color = #red "

def altura_to_pc(x):
    return x % 12

def altura_to_oct(x):
    return x // 12 - 1 #+3 #+3 temporario

def oitava_lilypond(n):
    result = ""
    if n >= 3:
        for i in range(n - 3):
            result += "'"
    else:
        for i in range(0, 3-n):
            result += ","
    return result

def altura_lilypond(pitch_class, oitava):
    #if oitava < 2:
    #    clef = '"bass_15"'
    if oitava < 4:
        clef = 'bass'
    else:#  oitava < 6:
        clef = 'treble'
    #else:
    #    clef = '"treble^15"'
    return '\\clef {0} {1}{2}'.format(clef, pitch_names[pitch_class],oitava_lilypond(oitava))

def gerar_markup(evento, niveis_spec):
    markup = ""
    for i in range(len(evento.niveis)):
        if evento.niveis[i]:
            markup += niveis_spec[i] + str(evento.niveis[i])
    if markup:
        markup = "^\\markup{{{0}}}".format(markup)
    return markup


class Nota:
    def __init__(self, altura, duracao, markup):
        self.pitch_class = altura_to_pc(altura)
        self.oitava = altura_to_oct(altura)
        self.duracao = duracao
        self.markup = markup

    def string_lily(self):
        cor = ""
        if self.markup:
            cor = red
        return duracoes_string[self.duracao].format(
            altura_lilypond(self.pitch_class, self.oitava), mp=self.markup, cor=cor)

class Quialtera:
    def __init__(self, altura, duracao, markup_list):
        self.pitch_class = []
        self.oitava = []
        for i in altura:
            self.pitch_class.append(altura_to_pc(i))
            self.oitava.append(altura_to_oct(i))
        self.duracao = duracao
        self.markup = markup_list

    def string_lily(self):
        alturas = []
        cor = []
        for i in range(len(self.pitch_class)):
            alturas.append(altura_lilypond(self.pitch_class[i], self.oitava[i]))
            if self.markup[i]:
                cor.append(red)
            else:
                cor.append("")
        return duracoes_string[self.duracao].format(*alturas, mp=self.markup, cor=cor)

def processar_eventos(eventos, niveis_spec):
    lily_lista = []
    i = 0
    while i < len(eventos):
        alt = eventos[i].altura
        dur = eventos[i].duracao
        if dur in quialteras_n:
            n = quialteras_n[dur]+i
            alturas_quialtera = []
            markup_list = []
            while i < n:
                alturas_quialtera.append(eventos[i].altura)
                markup_list.append(gerar_markup(eventos[i], niveis_spec))
                i += 1
            lily_lista.append(Quialtera(alturas_quialtera, dur, markup_list))
        else:
            lily_lista.append(Nota(alt,dur,gerar_markup(eventos[i], niveis_spec)))
            i += 1
    return lily_lista

def gerar_lilypond(arquivo, eventos, niveis_spec):
    notas = processar_eventos(eventos, niveis_spec)
    with open(arquivo, mode='w', encoding='UTF-8') as output:
        output.write("\\new Voice {\n\\override Staff.TimeSignature #'stencil = ##f\n\\cadenzaOn\n")
        last = len(notas)-1
        for i in range(len(notas)):
            output.write(notas[i].string_lily())
            if i == last:
                output.write(' \\bar "|."\n')
            else:
                output.write(' \\bar ""\n')
        output.write("\\cadenzaOff \n}")
