from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import arquivo
import randomicos
import gestalt

def gerar(quantidade_string):
    if quantidade_string == "":
        input_arquivo = filedialog.askopenfilename(filetypes=[("All files", "*")])
        if input_arquivo == "":
            return
        obj = arquivo.abrir(input_arquivo)
    else:
        try:
            obj = randomicos.Aleatorio(int(quantidade_string))
        except ValueError:
            return
    arquivo_output = filedialog.asksaveasfilename(defaultextension='.ly', filetypes=[("Lilypond", "*.ly"), ("All files", "*")])
    if arquivo_output == "":
        return
    gestalt.gerar(arquivo_output, obj)

root = Tk()
root.title("Gestalt")
root.geometry('+100+100')
frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

quantidade = StringVar()

quant_entry = ttk.Entry(frame, width=7, textvariable=quantidade)
quant_entry.grid(column=2, row=1, sticky=(W, E))
ttk.Button(frame, text="Gerar", command=lambda: gerar(quantidade.get())).grid(column=3, row=3, sticky=W)
ttk.Label(frame, text="Quantidade").grid(column=3, row=1, sticky=W)

for child in frame.winfo_children():
    child.grid_configure(padx = 5, pady = 5)

quant_entry.focus()

root.mainloop()
