from tkinter import *
from tkinter import *


class Chrono():
    
    def resetChrono(self):
        self.count=1
        self.t.set('00:00:00')
        
    def startChrono(self):
        self.count=0
        self.timerChrono()

    def stopChrono(self):
        self.count=1
        
        
    def timerChrono(self):
        if(self.count==0):
            self.d = str(self.t.get())
            h,m,s = map(int,self.d.split(":"))
            
            h = int(h)
            m=int(m)
            s= int(s)
            if(s<59):
                s+=1
            elif(s==59):
                s=0
                if(m<59):
                    m+=1
                elif(m==59):
                    h+=1
            if(h<10):
                h = str(0)+str(h)
            else:
                h= str(h)
            if(m<10):
                m = str(0)+str(m)
            else:
                m = str(m)
            if(s<10):
                s=str(0)+str(s)
            else:
                s=str(s)
            self.d=h+":"+m+":"+s
            
            
            self.t.set(self.d)
            if(self.count==0):
                self.root.after(1000,self.timerChrono)
            
        
    def __init__(self, fenetre):
        self.root=fenetre
        self.t = StringVar()
        self.t.set("00:00:00")
        self.lb = Label(self.root,textvariable=self.t)
        self.lb.pack()
        self.count=1

        
        
    
    

