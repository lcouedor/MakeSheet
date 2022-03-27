import tkinter
from timeit import default_timer
from lib import resource_path

class Chrono():
    
    #Fonction qui remet à zéro le chrono
    def resetChrono(self):
        self.count=1
        self.t.set('00:00')
    
    #Fonction qui lance le chrono
    def startChrono(self):
        self.count=0
        self.start = default_timer()
        self.timerChrono()

    #Focntion qui stop le chrono
    def stopChrono(self):
        self.count=1
        
    #Fonction qui calcul le temps
    def timerChrono(self):
        if(self.count==0):
            now = default_timer() - self.start
            minutes, seconds = divmod(now, 60)
            minutes=int(minutes)
            seconds=int(seconds)
            if(minutes<10):
                minutes = str(0)+str(minutes)
            if(seconds<10):
                seconds=str(0)+str(seconds)
            self.t.set(str(minutes)+":"+str(seconds))
            if(self.count==0):
                self.root.after(1000,self.timerChrono)
            
        
    def __init__(self, fenetre):
        self.root=fenetre
        #Initialisation du texte variable
        self.t = tkinter.StringVar()
        self.t.set("00:00")
        self.frameChrono=tkinter.Frame(self.root)
        #Initialisation de l'image
        self.imageChrono=tkinter.PhotoImage(file=resource_path('images/chrono.png'))
        self.labelImage=tkinter.Label(self.frameChrono,image=self.imageChrono)
        self.labelImage.config(background="#D9D9D9")
        self.lb = tkinter.Label(self.frameChrono,textvariable=self.t)
        self.lb.grid(row=0,column=1)
        self.labelImage.grid(row=0,column=0)
        self.lb.config(background="#D9D9D9",font=20)
        self.frameChrono.grid(row=0,column=1,sticky='WE')
        self.frameChrono.config(background="#D9D9D9")
        self.start=0
        self.count=1

        
        
    
    

