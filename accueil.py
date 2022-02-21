from cProfile import label
import numpy as np
from back import *
from ParametresPage import *
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk

  
class Accueil():
    def __init__(self,fenetre,pa):
        self.fenetre=fenetre
        self.label = Label(self.fenetre)
        self.label["text"]="Accueil"
        self.label.config(background="#D9D9D9",font=30)
        self.label.grid(row=0,column=0,padx=0, pady=20)
        self.pa=pa
        self.frameTot=Frame(self.fenetre)
        self.imLogo= PIL.Image.open("images/logo.png")
        self.resolution = (250,250)    
        self.logoImage= PIL.ImageTk.PhotoImage(self.imLogo.resize(self.resolution))
        self.imlabel=Label(self.frameTot,image=self.logoImage)
        self.imlabel.grid(row=0,column=1)
        self.imlabel.config(background="#D9D9D9")
        self.frameTextes=Frame(self.frameTot)
        self.textePresentation = Label(self.frameTextes,wraplength=300)
        self.textePresentation["text"]="L'application MakeSheet est application composé d'un accordeur et d'un générateur de partition. Celle-ci a été conçu par Couedor Léo et Sorin Alexia"
        self.textePresentation.config(background="#D9D9D9")
        self.textePresentation.grid(row=0,column=0)
        self.texteTuner = Label(self.frameTextes,wraplength=300)
        self.texteTuner["text"]="La fenêtre Tuner permet d'accèder à l'accordeur. Appuyez sur lancer pour lancer l'accordeur et sur stop pour le stopper. Au cours de l'éxécution vous verrez() la note détectée ainsi que l'écart avec la note absolue afin de pouvoir régler votre instrument."
        self.texteTuner.config(background="#D9D9D9")
        self.texteTuner.grid(row=1,column=0)
        self.textePartition = Label(self.frameTextes,wraplength=300)
        self.textePartition["text"]="La fenêtre Partition permet d'accèder au générateur de partition. Afin de pouvoir lancer le générateur remplissez tout les champs puis appuyez sur lancer. Lors de l'éxécution un chronomètre est affiché afin de savoir depuis quand l'enregistrement est en route. Pour stopper le générateur, appuyez sur Stop."
        self.textePartition.config(background="#D9D9D9")
        self.textePartition.grid(row=2,column=0)
        self.texteParam = Label(self.frameTextes,wraplength=300)
        self.texteParam["text"]="La fenêtre Paramètres permet d'accèder au paramètes en liens avec les différents chemins vers les différents fichiers. Cela vous permets de voir et/ou modifier ceux-ci."
        self.texteParam.config(background="#D9D9D9")
        self.texteParam.grid(row=3,column=0)
        self.frameTextes.grid(row=0,column=0)
        self.frameTextes.config(background="#D9D9D9")
        self.frameTot.grid(row=1, column=0)
        self.frameTot.config(background="#D9D9D9")
        self.fenetre.grid_columnconfigure(0,weight=1)
        self.fenetre.grid_rowconfigure(1,weight=1)
        self.frameTot.grid_columnconfigure(0,weight=1)
        self.frameTot.grid_columnconfigure(1,weight=1)
        self.frameTot.grid_rowconfigure(0,weight=1)
        self.frameTextes.grid_columnconfigure(0,weight=1)
        self.frameTextes.grid_rowconfigure(0,weight=1)
        self.frameTextes.grid_rowconfigure(1,weight=1)
        self.frameTextes.grid_rowconfigure(2,weight=1)
        self.frameTextes.grid_rowconfigure(3,weight=1)
        self.frameTextes.grid(sticky='NS')
        self.frameTot.grid(sticky="EWNS")


    
    
    
    
    


