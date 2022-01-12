from tkinter import *
from timeit import default_timer

class Chrono():
    
    def resetChrono(self):
        self.count=1
        self.t.set('00:00')
        
    def startChrono(self):
        self.count=0
        self.start = default_timer()
        self.timerChrono()

    def stopChrono(self):
        self.count=1
        
        
    def timerChrono(self):
        if(self.count==0):
            # self.d = str(self.t.get())
            # m,s = map(int,self.d.split(":"))
            
            # m=int(m)
            # s= int(s)
            # if(s<59):
            #     s+=1
            # elif(s==59):
            #     s=0
            #     if(m<59):
            #         m+=1
            # if(m<10):
            #     m = str(0)+str(m)
            # else:
            #     m = str(m)
            # if(s<10):
            #     s=str(0)+str(s)
            # else:
            #     s=str(s)
            # self.d=m+":"+s
            
            
            # self.t.set(self.d)
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
        self.t = StringVar()
        self.t.set("00:00")
        self.lb = Label(self.root,textvariable=self.t)
        self.lb.pack()
        self.start=0
        self.count=1

        
        
    
    

