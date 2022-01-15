from tkinter import *
from TunerPage import *
import pyaudio
from PartitionPage import Partition
from accueil import Accueil
from ParametresPage import Parametre
from back import *

def TunerPageFct():
    frameAccueil.pack_forget()
    framePartition.pack_forget()
    frameParametres.pack_forget()
    frameTuner.pack()
    pr.pause()
        
def PartitionPageFct():
    frameAccueil.pack_forget()
    frameTuner.pack_forget()
    frameParametres.pack_forget()
    framePartition.pack()
    t.pause()

def AccueilPageFct():
    framePartition.pack_forget()
    frameTuner.pack_forget()
    frameParametres.pack_forget()
    frameAccueil.pack()
    a.miseAjour()
    t.pause()
    pr.pause()

def ParametrePageFct():
    framePartition.pack_forget()
    frameTuner.pack_forget()
    frameAccueil.pack_forget()
    frameParametres.pack()
    t.pause()
    pr.pause()


fenetre = Tk()#Création de la fenêtre 
fenetre.title("Make Sheet")#Nom de la fenêtre
fenetre.geometry("1080x720")#Dimension de la fenêtre
fenetre.config(background="WHITE")#Couleur du background
frameBouton= Frame(fenetre)#création de la zone de bouton
frameBouton.config(background="WHITE")
accueil=Button(frameBouton, text="Accueil Page", command=AccueilPageFct)#Bouton pour accéder à l'accueil
tuner=Button(frameBouton, text="Tuner Page", command=TunerPageFct)#Bouton pour accèder à l'accordeur
partition=Button(frameBouton, text="Partition Page", command=PartitionPageFct)#Bouton pour accèder à la partition
parametre=Button(frameBouton, text="Paramètres Page", command=ParametrePageFct)#Bouton pour accèder à la partition
accueil.pack()
tuner.pack()
partition.pack()
parametre.pack()
frameBouton.pack()
#Création des frames pour les différentes page que l'on ajoutera ou supprimera de la fenetre en fonction de la page demandée
p = pyaudio.PyAudio() #Instanciation de PyAudio
frameAccueil = Frame(fenetre)
frameAccueil.config(background="WHITE")
frameAccueil.pack()
frameParametres = Frame(fenetre)
frameParametres.config(background="WHITE")
pa=Parametre(frameParametres)
a=Accueil(frameAccueil,pa)
frameTuner = Frame(fenetre)
frameTuner.config(background="WHITE")
t=Tuner(frameTuner,p)
t.start()
framePartition = Frame(fenetre)
framePartition.config(background="WHITE")
pr=Partition(framePartition,p)
pr.start()
fenetre.mainloop()