from tkinter import *
from TunerPage import *
import pyaudio
from PartitionPage import Partition
from accueil import Accueil
from ParametresPage import Parametre
from back import *
import PIL.Image
import PIL.ImageTk

def TunerPageFct():
    frameAccueil.grid_forget()
    framePartition.grid_forget()
    frameParametres.grid_forget()
    accueil.config(fg="BLACK")
    partition.config(fg="BLACK")
    parametre.config(fg="BLACK")
    tuner.config(fg="#B38C30")
    frameTuner.grid(row=1,sticky='EWNS')
    pr.pause()
        
def PartitionPageFct():
    frameAccueil.grid_forget()
    frameTuner.grid_forget()
    frameParametres.grid_forget()
    accueil.config(fg="BLACK")
    tuner.config(fg="BLACK")
    parametre.config(fg="BLACK")
    partition.config(fg="#B38C30")
    framePartition.grid(row=1,sticky='EWNS')
    t.pause()

def AccueilPageFct():
    framePartition.grid_forget()
    frameTuner.grid_forget()
    frameParametres.grid_forget()
    tuner.config(fg="BLACK")
    partition.config(fg="BLACK")
    parametre.config(fg="BLACK")
    accueil.config(fg="#B38C30")
    frameAccueil.grid(row=1,sticky='EWNS')
    a.miseAjour()
    t.pause()
    pr.pause()

def ParametrePageFct():
    framePartition.grid_forget()
    frameTuner.grid_forget()
    frameAccueil.grid_forget()
    accueil.config(fg="BLACK")
    partition.config(fg="BLACK")
    tuner.config(fg="BLACK")
    parametre.config(fg="#B38C30")
    frameParametres.grid(row=1,sticky='EWNS')
    t.pause()
    pr.pause()


fenetre = Tk()#Création de la fenêtre 
fenetre.title("Make Sheet")#Nom de la fenêtre
fenetre.geometry("1080x720")#Dimension de la fenêtre
fenetre.minsize(width=800, height=550)
fenetre.grid_columnconfigure(0,weight=1)
fenetre.grid_rowconfigure(1,weight=1)
fenetre.config(background="WHITE")#Couleur du background
frameBouton= Frame(fenetre)#création de la zone de bouton
frameBouton.config(background="WHITE")
imLogo= PIL.Image.open("images/logo.png")
resolution = (60,60)
logoImage= PIL.ImageTk.PhotoImage(imLogo.resize(resolution))
homeImage=PhotoImage(file='images/accueil.png')
tunerImage=PhotoImage(file='images/tuner.png')
partitionImage=PhotoImage(file='images/partition.png')
parametreImage=PhotoImage(file='images/parametres.png')
logo=Label(frameBouton,image=logoImage, background="WHITE")
accueil=Button(frameBouton, text="Accueil",image=homeImage,compound='top', command=AccueilPageFct, background="WHITE", bd=0, fg="#B38C30")#Bouton pour accéder à l'accueil
tuner=Button(frameBouton, text="Tuner",image=tunerImage,compound='top', command=TunerPageFct,  background="WHITE", bd=0)#Bouton pour accèder à l'accordeur
partition=Button(frameBouton, text="Partition",image=partitionImage,compound='top', command=PartitionPageFct, background="WHITE", bd=0)#Bouton pour accèder à la partition
parametre=Button(frameBouton, text="Paramètres",image=parametreImage,compound='top', command=ParametrePageFct, background="WHITE", bd=0)#Bouton pour accèder à la partition
logo.grid(row=0,column=0,sticky='WN')
accueil.grid(row=0,column=1,sticky='EN')
tuner.grid(row=0,column=2,sticky='EN')
partition.grid(row=0,column=3,sticky='EN')
parametre.grid(row=0,column=4,sticky='EN')
frameBouton.grid(row=0,sticky='EWN')
frameBouton.grid_columnconfigure(0,weight=3)
frameBouton.grid_columnconfigure(1,weight=1)
frameBouton.grid_columnconfigure(2,weight=1)
frameBouton.grid_columnconfigure(3,weight=1)
frameBouton.grid_columnconfigure(4,weight=1)
#Création des frames pour les différentes page que l'on ajoutera ou supprimera de la fenetre en fonction de la page demandée
p = pyaudio.PyAudio() #Instanciation de PyAudio
frameAccueil = Frame(fenetre)
frameAccueil.config(background="#D9D9D9")
frameAccueil.grid(row=1,sticky='EWNS')
frameParametres = Frame(fenetre)
frameParametres.config(background="#D9D9D9")
pa=Parametre(frameParametres)
a=Accueil(frameAccueil,pa)
frameTuner = Frame(fenetre)
frameTuner.config(background="#D9D9D9")
t=Tuner(frameTuner,p)
t.start()
framePartition = Frame(fenetre)
framePartition.config(background="#D9D9D9")
pr=Partition(framePartition,p)
pr.start()
fenetre.mainloop()