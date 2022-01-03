import threading
import numpy as np
from back import *
from tkinter import *
from tkinter import ttk


  
class Accueil(threading.Thread):
    def __init__(self,fenetre):
        threading.Thread.__init__(self)
        self.fenetre=fenetre
        self.label = Label(self.fenetre)
        self.label["text"]="Accueil"
        self.label.config(background="WHITE")
        self.label.pack()
    
    
    
    


