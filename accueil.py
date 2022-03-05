import tkinter
import PIL.Image
import PIL.ImageTk

from lib import resource_path
  
class Accueil():
    def __init__(self,fenetre,pa):
        self.fenetre=fenetre
        self.label = tkinter.Label(self.fenetre)
        self.label["text"]="Accueil"
        self.label.config(background="#D9D9D9",font=30)
        self.label.grid(row=0,column=0,padx=0, pady=20)
        self.pa=pa
        self.frameTot=tkinter.Frame(self.fenetre)
        self.imLogo= PIL.Image.open(resource_path("images/logo.png"))
        self.resolution = (250,250)    
        self.logoImage= PIL.ImageTk.PhotoImage(self.imLogo.resize(self.resolution))
        self.imlabel=tkinter.Label(self.frameTot,image=self.logoImage)
        self.imlabel.grid(row=0,column=1)
        self.imlabel.config(background="#D9D9D9")
        self.frameTextes=tkinter.Frame(self.frameTot)
        self.textePresentation = tkinter.Label(self.frameTextes,wraplength=300)
        self.textePresentation["text"]="L'application MakeSheet est une application composée d'un accordeur et d'un générateur de partition. Celle-ci a été conçue par Léo Couedor et Alexia Sorin"
        self.textePresentation.config(background="#D9D9D9")
        self.textePresentation.grid(row=0,column=0)
        self.texteTuner = tkinter.Label(self.frameTextes,wraplength=300)
        self.texteTuner["text"]="La fenêtre Tuner permet d'accéder à l'accordeur. Appuyez sur lancer pour lancer l'accordeur et sur stop pour le stopper. Au cours de l'éxécution vous verrez la note détectée ainsi que l'écart avec la note parfaitement accordée afin de pouvoir accorder votre instrument."
        self.texteTuner.config(background="#D9D9D9")
        self.texteTuner.grid(row=1,column=0)
        self.textePartition = tkinter.Label(self.frameTextes,wraplength=300)
        self.textePartition["text"]="La fenêtre Partition permet d'accéder au générateur de partition. Afin de pouvoir lancer le générateur, remplissez tout les champs puis appuyez sur lancer. Lors de l'exécution, un chronomètre est affiché afin de connaitre la durée de l'enregistrement. Pour stopper le générateur, appuyez sur Stop."
        self.textePartition.config(background="#D9D9D9")
        self.textePartition.grid(row=2,column=0)
        self.texteParam = tkinter.Label(self.frameTextes,wraplength=300)
        self.texteParam["text"]="La fenêtre Paramètres permet d'accéder aux paramètes en lien avec les différents emplacements de fichiers. Cela vous permets de voir et de modifier ceux-ci."
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


    
    
    
    
    


