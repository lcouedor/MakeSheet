from back import *
from tkinter import *
import tkinter.filedialog
import os

class Parametre():

    def __init__(self,fenetre):
        self.fenetre=fenetre #correspond à la fenetre de la page du tuner
        self.label = Label(self.fenetre) #correspond au label qui affiche la note
        self.user=os.getlogin()

        fichier = open('serial/file', 'r')
        musescore = open('serial/musescore', 'r')

        self.cheminFichier=str(fichier.read())
        self.cheminMuseScore=str(musescore.read())

        fichier.close()
        musescore.close()

        self.label["text"]="Paramètres"
        self.label.config(background="#D9D9D9", font=30)
        self.label.grid(row=0,column=0,padx=0, pady=20)
        self.frameParam=Frame(self.fenetre)
        self.LabelFichier = Label(self.frameParam, text="Chemin du fichier   ->   "+self.cheminFichier)
        self.LabelFichier.config(background="#D9D9D9")
        self.LabelFichier.grid(row=0,column=0,padx=20, pady=0)
        self.bouton_ValideF = Button(self.frameParam, text="Séléctionner", command=self.validerFichier,  background="#B38C30", fg="WHITE") 
        self.bouton_ValideF.grid(row=0,column=1)
        self.LabelMuseScore = Label(self.frameParam, text="Chemin de MuseScore   ->   "+self.cheminMuseScore)
        self.LabelMuseScore.grid(row=1,column=0,padx=20, pady=0)
        self.LabelMuseScore.config(background="#D9D9D9")
        self.bouton_ValideM = Button(self.frameParam, text="Sélectionner", command=self.validerMuseScore,  background="#B38C30", fg="WHITE") 
        self.bouton_ValideM.grid(row=1,column=1)
        self.frameParam.grid(row=1,column=0)
        self.erreur = Label(self.fenetre) 
        self.erreur["text"]=""
        self.erreur.config(background="#D9D9D9",fg="RED")
        self.erreur.grid(row=2,column=0)
        self.fenetre.grid_columnconfigure(0,weight=1)
        self.fenetre.grid_rowconfigure(1,weight=1)
        self.fenetre.grid_rowconfigure(2,weight=1)
        self.frameParam.grid_columnconfigure(0,weight=1)
        self.frameParam.grid_columnconfigure(1,weight=1)
        self.frameParam.grid_rowconfigure(0,weight=1)
        self.frameParam.grid_rowconfigure(0,weight=1)
        self.frameParam.config(background="#D9D9D9")
        self.frameParam.grid(sticky='NS')

    def validerFichier(self):
        cf= tkinter.filedialog.askdirectory ( title = "Sélectionnez un répertoire de destination ..." , mustexist = True, initialdir=self.cheminFichier )
        if len(cf) > 0:
            self.cheminFichier=cf
            self.LabelFichier["text"]="Chemin du fichier : "+self.cheminFichier
            fichier = open('serial/file', 'w+')
            fichier.truncate(0)
            fichier.write(self.cheminFichier+"/")
    
    def validerMuseScore(self):
        cc=tkinter.filedialog.askdirectory ( title = "Sélectionnez le répertoire bin de MuseScore ..." , mustexist = True, initialdir=self.cheminMuseScore )
        if len(cc) > 0:
            self.cheminMuseScore=cc
            self.LabelMuseScore["text"]="Chemin de MuseScore : "+self.cheminMuseScore
            fichier = open('serial/musescore', 'w+')
            fichier.truncate(0)
            fichier.write(self.cheminMuseScore)
        
        
        

    