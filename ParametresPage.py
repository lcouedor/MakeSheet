from back import *
from tkinter import *
import tkinter.filedialog
import os


class Parametre():

    def __init__(self,fenetre):
        self.fenetre=fenetre #correspond à la fenetre de la page du tunner
        self.label = Label(self.fenetre) #correspond au label qui affiche la note
        self.user=os.getlogin()
        self.cheminFichier="C:\\Users\\" + os.getlogin() + "\\Documents"
        self.cheminMuseScore="C:\\Users\\" + os.getlogin() + "\\Documents\\MuseScore3"
        self.label["text"]="Paramètres"
        self.label.config(background="WHITE")
        self.label.pack()
        self.LabelFichier = Label(fenetre, text="Chemin du fichier : "+self.cheminFichier)
        self.LabelFichier.config(background="WHITE")
        self.LabelFichier.pack()
        self.bouton_ValideF = Button(fenetre, text="Séléctionner un nouvel l'emplacement du fichier", command=self.validerFichier) 
        self.bouton_ValideF.pack()
        self.LabelMuseScore = Label(fenetre, text="Chemin de MuseScore : "+self.cheminMuseScore)
        self.LabelMuseScore.pack()
        self.LabelMuseScore.config(background="WHITE")
        self.bouton_ValideM = Button(fenetre, text="Sélectionner un nouvel l'emplacement de MuseScore", command=self.validerMuseScore) 
        self.bouton_ValideM.pack()
        self.erreur = Label(self.fenetre) 
        self.erreur["text"]=""
        self.erreur.config(background="WHITE")
        self.erreur.pack()
       
        
    def validerFichier(self):
        cf= tkinter.filedialog.askdirectory ( title = "Sélectionnez un répertoire de destination ..." , mustexist = True, initialdir=self.cheminFichier )
        if len(cf) > 0:
            self.cheminFichier=cf
            self.LabelFichier["text"]="Chemin du fichier : "+self.cheminFichier
    
    def validerMuseScore(self):
        cc=tkinter.filedialog.askdirectory ( title = "Sélectionnez un répertoire de destination ..." , mustexist = True, initialdir=self.cheminMuseScore )
        if len(cc) > 0:
            self.cheminMuseScore=cc
            self.LabelMuseScore["text"]="Chemin de MuseScore : "+self.cheminMuseScore
        
        
        

    