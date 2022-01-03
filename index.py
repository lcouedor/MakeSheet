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


fenetre = Tk()#Création de la fenêtre 
fenetre.title("Make Sheet")#Nom de la fenêtre
fenetre.geometry("1080x720")#Dimension de la fenêtre
fenetre.config(background="WHITE")#Couleur du background
frameBouton= Frame(fenetre)#création de la zone de bouton
frameBouton.config(background="WHITE")
accueil=Button(frameBouton, text="Accueil Page", command=AccueilPageFct)#Bouton pour accèder à l'accueil
tuner=Button(frameBouton, text="Tuner Page", command=TunerPageFct)#Bouton pour accèder à l'accordeur
partition=Button(frameBouton, text="Partition Page", command=PartitionPageFct)#Bouton pour accèder à la partition
accueil.pack()
tuner.pack()
partition.pack()
frameBouton.pack()
#Création des frames pour les différentes page que l'on ajoutera ou supprimera de la fenetre en fonction de la page demandée
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