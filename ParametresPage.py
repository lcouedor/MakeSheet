from back import *
from tkinter import *
import tkinter.filedialog


class Parametre():

    def __init__(self,fenetre):
        self.fenetre=fenetre #correspond à la fenetre de la page du tunner
        self.label = Label(self.fenetre) #correspond au label qui affiche la note
        self.cheminFichier=""
        self.cheminMuseScore=""
        self.label["text"]="Paramètres"
        self.label.config(background="WHITE")
        self.label.pack()
        self.LabelFichier = Label(fenetre, text="Chemin du fichier : "+self.cheminFichier)
        self.LabelFichier.pack()
        self.bouton_ValideF = Button(fenetre, text="Séléctionner un nouvel l'emplacement du fichier", command=self.validerFichier) 
        self.bouton_ValideF.pack()
        self.LabelMuseScore = Label(fenetre, text="Chemin de MuseScore : "+self.cheminMuseScore)
        self.LabelMuseScore.pack()
        self.bouton_ValideM = Button(fenetre, text="Sélectionner un nouvel l'emplacement de MuseScore", command=self.validerMuseScore) 
        self.bouton_ValideM.pack()
        self.erreur = Label(self.fenetre) 
        self.erreur["text"]=""
        self.erreur.config(background="WHITE")
        self.erreur.pack()
       
        
    def validerFichier(self):
        self.cheminFichier= tkinter.filedialog.askdirectory ( title = "Sélectionnez un répertoire de destination ..." , mustexist = True )
        self.LabelFichier["text"]="Chemin du fichier : "+self.cheminFichier
    
    def validerMuseScore(self):
        self.cheminMuseScore=tkinter.filedialog.askdirectory ( title = "Sélectionnez un répertoire de destination ..." , mustexist = True )
        self.LabelMuseScore["text"]="Chemin de MuseScore : "+self.cheminMuseScore
        
        
        

    