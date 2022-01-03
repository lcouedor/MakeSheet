import threading
import numpy as np
from back import *
from tkinter import *

class Partition(threading.Thread):
    def __init__(self,fenetre):
        threading.Thread.__init__(self)
        self.fenetre=fenetre
        self.label = Label(self.fenetre)
        self.label["text"]="Partition"
        self.label.config(background="WHITE")
        self.label.pack()
        
    
    def run(self):
        self.label["text"]="test"



