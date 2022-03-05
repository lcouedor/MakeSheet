import tkinter
import pyaudio
import PIL.Image
import PIL.ImageTk
import os

from PartitionPage import Partition
from TunerPage import Tuner
from accueil import Accueil
from ParametresPage import Parametre
from lib import resource_path

#TODO quelque part dans le programme il doit y avoir un open pas fermé je crois

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
    #a.miseAjour() #TODO y a pas ça dans le code, c'est quoi ?
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

def Setup():
    if(not(os.path.isdir('serial'))):
        os.mkdir("./serial")

    if(os.path.exists("serial/file")):
        fichier = open('serial/file', 'r')
        fic = str(fichier.read())
        if(len(fic) == 0):
            fichier.close()
            fichier = open('serial/file', 'w')
            fichier.write("C:\\Users\\" + os.getlogin() + "\\Downloads\\")
            fichier.close()
    else:
        fichier = open('serial/file', 'w')
        fichier.write("C:\\Users\\" + os.getlogin() + "\\Downloads\\")
        fichier.close()
        
    if(os.path.exists("serial/musescore")):
        musescore = open('serial/musescore', 'r')
        muse = str(musescore.read())
        if(len(muse) == 0):
            musescore.close()
            musescore = open('serial/musescore', 'w')
            musescore.write("C:\\Program Files\\MuseScore 3\\bin\\")
            musescore.close()
    else:
        musescore = open('serial/musescore', 'w')
        musescore.write("C:\\Program Files\\MuseScore 3\\bin\\")
        musescore.close()

Setup() #Initialiser les fichiers d'emplacement de file et musescore, les créé si n'existent pas ou si contenu vide, idem pour le dossier serial

fenetre = tkinter.Tk()#Création de la fenêtre 
fenetre.title("Make Sheet")#Nom de la fenêtre
fenetre.geometry("1080x720")#Dimension de la fenêtre
fenetre.tk.call('wm','iconphoto',fenetre._w, tkinter.PhotoImage(file='images/logo.png'))
fenetre.minsize(width=800, height=550)
fenetre.grid_columnconfigure(0,weight=1)
fenetre.grid_rowconfigure(1,weight=1)
fenetre.config(background="WHITE")#Couleur du background
frameBouton= tkinter.Frame(fenetre)#création de la zone de bouton
frameBouton.config(background="WHITE")
imLogo= PIL.Image.open(resource_path("images/logo.png"))
resolution = (60,60)
logoImage= PIL.ImageTk.PhotoImage(imLogo.resize(resolution))
homeImage=tkinter.PhotoImage(file=resource_path('images/accueil.png'))
tunerImage=tkinter.PhotoImage(file=resource_path('images/tuner.png'))
partitionImage=tkinter.PhotoImage(file=resource_path('images/partition.png'))
parametreImage=tkinter.PhotoImage(file=resource_path('images/parametres.png'))
logo=tkinter.Label(frameBouton,image=logoImage, background="WHITE")
accueil=tkinter.Button(frameBouton, text="Accueil",image=homeImage,compound='top', command=AccueilPageFct, background="WHITE", bd=0, fg="#B38C30", cursor="hand2")#Bouton pour accéder à l'accueil
tuner=tkinter.Button(frameBouton, text="Tuner",image=tunerImage,compound='top', command=TunerPageFct,  background="WHITE", bd=0, cursor="hand2")#Bouton pour accèder à l'accordeur
partition=tkinter.Button(frameBouton, text="Partition",image=partitionImage,compound='top', command=PartitionPageFct, background="WHITE", bd=0, cursor="hand2")#Bouton pour accèder à la partition
parametre=tkinter.Button(frameBouton, text="Paramètres",image=parametreImage,compound='top', command=ParametrePageFct, background="WHITE", bd=0, cursor="hand2")#Bouton pour accèder à la partition
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
frameAccueil = tkinter.Frame(fenetre)
frameAccueil.config(background="#D9D9D9")
frameAccueil.grid(row=1,sticky='EWNS')
frameParametres = tkinter.Frame(fenetre)
frameParametres.config(background="#D9D9D9")
pa=Parametre(frameParametres)
a=Accueil(frameAccueil,pa)
frameTuner = tkinter.Frame(fenetre)
frameTuner.config(background="#D9D9D9")
t=Tuner(frameTuner,p)
t.start()
framePartition = tkinter.Frame(fenetre)
framePartition.config(background="#D9D9D9")
pr=Partition(framePartition,p)
pr.start()
fenetre.mainloop()