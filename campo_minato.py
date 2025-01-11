import tkinter as tk
import random as rnd
from tkinter import messagebox 
from tkinter import ttk

root = tk.Tk()
root.title("Campo-Minato")
root.resizable(False, False)
root.config(background="#f5e7b0")

r = 8
c = 10
bombe = 30
bandiere = bombe
celle_da_scoprire = r*c - bombe
griglia = []
bombe_create = False
Difficolta = ['Facile','Medio','Difficile']
direzioni = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
tempo_iniziato = False
tempo = 0

frame_superiore = tk.Frame(root,background="#f5e7b0")
frame_superiore.grid(row=0, column=0, columnspan=c, pady=10)

timer_label = tk.Label(frame_superiore, text=f"Tempo: {tempo}", bg="#f5e7b0", font=('Times New Roman', 12, 'bold'))
timer_label.grid(row=0, column=1)

bandiere_label = tk.Label(frame_superiore, text=f"Bandiere: {bandiere}", bg="#f5e7b0", font=('Times New Roman', 12, 'bold'))
bandiere_label.grid(row=0, column=2)

def aggiorna_timer():
    global tempo, tempo_iniziato
    if tempo_iniziato:
        tempo += 1
        timer_label.config(text=f"Tempo: {tempo}s")
        root.after(1000, aggiorna_timer)

def cambia_difficolta():
    global bombe, bandiere, celle_da_scoprire, bombe_create, griglia, tempo, tempo_iniziato, r, c
    
    diff = combo.get()
    if diff == 'Facile':
        r = 6
        c = 8
        bombe = 15
    elif diff == "Medio":
        r = 8
        c = 10
        bombe = 35
    elif diff == "Difficile":
        r = 10
        c = 12
        bombe = 50

    bandiere = bombe
    bandiere_label.config(text=f"Bandiere: {bandiere}")
    celle_da_scoprire = r * c - bombe
    bombe_create = False
    tempo_iniziato = False
    tempo = 0
    timer_label.config(text=f"Tempo: {tempo}s")
    resetta_griglia(r, c)

def resetta_griglia(r, c):
    global griglia

    for i in range(len(griglia)):
        for j in range(len(griglia[i])):
            griglia[i][j]["bottone"].grid_forget()

    griglia = []
    crea_griglia(r, c)
    
def crea_griglia(r,c):
    global griglia
    for  i in range(r):
        root.grid_rowconfigure(i+1, weight=1)
        griglia.append([])
        for  j in range(c):
            root.grid_columnconfigure(j, weight=1)
            if  (i%2 == 0 and j%2 == 0) or (i%2 == 1 and j%2 == 1) :
                btn = tk.Button(root,width=4,height=2, background="#73EC8B", bd = 0, font=('Times New Roman', 11, 'bold')) 
            else:
                btn = tk.Button(root,width=4,height=2, background="#D2FF72", bd = 0, font=('Times New Roman', 11, 'bold'))
                          
            btn.grid(row=i+1,column=j, sticky="nsew")
            btn.bind("<Button-1>", scopri_ascoltatore)
            btn.bind("<Button-3>", posiziona_bandiera)
            dict = {"bottone" : btn,
                    "etichetta" : "B",
                    "scoperta" : False,
                    "bandiera": False}
            griglia[i].append(dict)

def crea_bombe(n_bomb, x, y):
    global griglia
    
    righe = len(griglia)
    colonne = len(griglia[0])

    celle_proibite = [(x, y)] + [(x + dx, y + dy) for dx, dy in direzioni if 0 <= x + dx < righe and 0 <= y + dy < colonne]

    posizionate = 0
    while posizionate < n_bomb:
        r = rnd.randrange(righe)
        c = rnd.randrange(colonne)
        
        if (r, c) not in celle_proibite and griglia[r][c]["etichetta"] != "💣":
            griglia[r][c]["etichetta"] = "💣"
            posizionate += 1

    conta_bombe()


    for r, c in celle_proibite:
        if 0 <= r < righe and 0 <= c < colonne:
            griglia[r][c]["etichetta"] = 0
            

def conta_bombe():
    global griglia
    
    righe = len(griglia)
    colonne = len(griglia[0])
    
    for i in range(righe):
        for j in range(colonne):
            if griglia[i][j]["etichetta"] != "💣":
                c = 0
                for dx, dy in direzioni:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < righe and 0 <= nj < colonne and griglia[ni][nj]["etichetta"] == "💣":
                        c += 1
                griglia[i][j]["etichetta"] = c
                if  c == 1:
                    griglia[i][j]["bottone"].config(fg="blue")
                elif c == 2:
                    griglia[i][j]["bottone"].config(fg="green")
                elif c == 3:
                    griglia[i][j]["bottone"].config(fg="red")
                elif c == 4:
                    griglia[i][j]["bottone"].config(fg="purple")
                elif c == 5:
                    griglia[i][j]["bottone"].config(fg="orange")
                elif c == 6:
                    griglia[i][j]["bottone"].config(fg="pink")
                elif c == 7:
                    griglia[i][j]["bottone"].config(fg="brown")
                elif c == 8:
                    griglia[i][j]["bottone"].config(fg="gray")
                    
def scopri_cella(x:int, y: int):
    global griglia
    global celle_da_scoprire
    
    if griglia[x][y]["bandiera"] == True:
        return
    if  (x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1) :    
        griglia[x][y]["bottone"].config(bg="#B99470") 
    else:
        griglia[x][y]["bottone"].config(bg="#FEFAE0")
    griglia[x][y]["scoperta"] = True
    
    if griglia[x][y]["etichetta"] == 0:
        griglia[x][y]["bottone"].config(text="")
    else:
        griglia[x][y]["bottone"].config(text=griglia[x][y]["etichetta"])

    if griglia[x][y]["etichetta"] == "💣":
        messagebox.showerror("Sconfitta","Hai perso (Cadel è deluso😢😢)")
        root.destroy()
    else:
        celle_da_scoprire -= 1
        if celle_da_scoprire == 0:
            messagebox.showinfo("Vittoria","Hai vinto! Cadel e' fiero di te😊")
            root.destroy()

    if griglia[x][y]["etichetta"] == 0:
        righe = len(griglia)
        colonne = len(griglia[0])

        for dx, dy in direzioni:
            ni, nj = x + dx, y + dy
            if 0 <= ni < righe and 0 <= nj < colonne and not griglia[ni][nj]["scoperta"]:
                scopri_cella(ni, nj)
                      
def scopri_ascoltatore(event):
    global griglia, bombe, bombe_create, tempo_iniziato

    x = event.widget.grid_info()["row"]-1
    y = event.widget.grid_info()["column"]
    
    if bombe_create == False:
        crea_bombe(bombe,x,y)
        conta_bombe()
        bombe_create = True
        
    if tempo_iniziato == False:
        tempo_iniziato = True
        aggiorna_timer()
    
    scopri_cella(x,y)
    
    

def posiziona_bandiera(event):
    global griglia
    global bandiere
    
    x = event.widget.grid_info()["row"]-1
    y = event.widget.grid_info()["column"]
    
    if griglia[x][y]["scoperta"] == False:
        if griglia[x][y]["bandiera"] == False and bandiere > 0:
            griglia[x][y]["bottone"].config(text="🚩")
            griglia[x][y]["bandiera"] = True
            bandiere -= 1
        elif griglia[x][y]["bandiera"] ==  True:
            griglia[x][y]["bottone"].config(text="")
            griglia[x][y]["bandiera"] = False
            bandiere += 1
        elif bandiere == 0:
            messagebox.showwarning("ATTENZIONE", "Bandiere esaurite")
        bandiere_label.config(text=f"Bandiere: {bandiere}")


crea_griglia(r,c)


combo = ttk.Combobox(frame_superiore, values=Difficolta, state="readonly",width=15)
combo.current(1)
combo.grid(row=0, column=0)
combo.bind("<<ComboboxSelected>>", lambda event: cambia_difficolta())


root.mainloop()