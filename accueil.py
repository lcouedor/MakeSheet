import numpy as np
from back import *
from ParametresPage import *
from tkinter import *
from tkinter import ttk


  
class Accueil():
    def __init__(self,fenetre,pa):
        self.fenetre=fenetre
        self.label = Label(self.fenetre)
        self.label["text"]="Accueil"
        self.fichier = Label(self.fenetre)
        self.museScore = Label(self.fenetre)
        self.label.config(background="WHITE")
        self.label.pack()
        self.fichier.pack()
        self.museScore.pack()
        self.pa=pa
    
    def miseAjour(self):
        global cheminFichier
        global cheminMuseScore
        self.fichier["text"]=self.pa.cheminFichier
        self.museScore["text"]=self.pa.cheminMuseScore
    
    
    
    


