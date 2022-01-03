import numpy as np
from tkinter import *
from tkinter import ttk
from TunerPage import *
from PartitionPage import Partition
from accueil import Accueil

def TunerPageFct():
    frameAccueil.pack_forget()
    framePartition.pack_forget()
    frameTuner.pack()
    t.start()
        
def PartitionPageFct():
    frameAccueil.pack_forget()
    frameTuner.pack_forget()
    framePartition.pack()
    t.pause()
    p.start()

def AccueilPageFct():
    framePartition.pack_forget()
    frameTuner.pack_forget()
    frameAccueil.pack()
    t.pause()
    a.start()


fenetre = Tk()
fenetre.title("Make Sheet")
fenetre.geometry("1080x720")
fenetre.config(background="WHITE")
frameBouton= Frame(fenetre)
frameBouton.config(background="WHITE")
accueil=Button(frameBouton, text="Accueil Page", command=AccueilPageFct)
tuner=Button(frameBouton, text="Tuner Page", command=TunerPageFct)
partition=Button(frameBouton, text="Partition Page", command=PartitionPageFct)
accueil.pack()
tuner.pack()
partition.pack()
frameBouton.pack()
frameAccueil = Frame(fenetre)
frameAccueil.config(background="WHITE")
frameAccueil.pack()
a=Accueil(frameAccueil)
frameTuner = Frame(fenetre)
frameTuner.config(background="WHITE")
t=Tuner(frameTuner)
framePartition = Frame(fenetre)
framePartition.config(background="WHITE")
p=Partition(framePartition)
fenetre.mainloop()