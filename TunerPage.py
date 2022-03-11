import threading
import pyaudio
import wave
import soundfile
import numpy as np
import tkinter
import time
import math
import os

import back

class Tuner(threading.Thread):
    def __init__(self,fenetre,p):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.enpause=True #variable booleaine pour savoir si il faut stopper ou continuer le programme
        self.fenetre=fenetre #correspond à la fenetre de la page du tunner
        self.label = tkinter.Label(self.fenetre) 
        self.label["text"]="Tunner"
        self.label.config(background="#D9D9D9", font=30)
        self.debTot=0 #variable qui contient la fréquence de la note précédente
        self.finTot=0 #variable qui contient la fréquence de la note suivante
        self.finNote=0 #variable qui contient la fréquence de la fin de l'intervalle des fréquences pour la note 
        self.debNote=0 #variable qui contient la fréquence de le début de l'intervalle des fréquences pour la note 
        self.ecart = tkinter.Label(self.fenetre)#correspond au label qui affiche l'écart entre la fréquence de la note et la fréquence obtenue
        self.ecart["text"]=""
        self.ecart.config(background="#D9D9D9")
        self.label.grid(row=0,column=1)
        self.ecart.grid(row=1,column=1)
        self.CAN_Zone = tkinter.Canvas ( self.fenetre , bg = "#D9D9D9" , height = 395 , width = 540, bd=0, highlightthickness=0 ) #canva qui va contenir le compteur
        self.CAN_Zone.grid(row=2,column=1)
        self.CAN_Zone_Total = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520 , start = 0 , extent = 180 , fill = "#CCD1D1",outline="" )#arc de cercle corresponant à la totalité du compteur
        self.CAN_Zone_Red = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520 , start=0, extent =0, fill = "#F0B27A",outline="")#arc de cercle corresponant à la partie avant l'intervalle de la note
        self.CAN_Zone_Green = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520   , start=0, extent =0, fill = "#82E0AA",outline="")#arc de cercle corresponant à l'intervalle de la note
        self.CAN_Zone_Yellow = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=0, extent =0, fill = "#F4D03F",outline="")#arc de cercle corresponant à la partie après l'intervalle de la note
        self.CAN_aiguille =0 #aiguille du compteur
        self.CAN_norm =0 #segment correspondant à la fréquence de la note
        self.legendeNote=self.CAN_Zone.create_text(60, 320, anchor="w",text ="Intervalle de la note" )
        self.rectangleNote=self.CAN_Zone.create_rectangle(10,310,40,330, fill = "#82E0AA")
        self.legendeNotePrec=self.CAN_Zone.create_text(60, 350, anchor="w",text = "Intervalle de la note précédente" )
        self.rectangleNote=self.CAN_Zone.create_rectangle(10,340,40,360,fill = "#F0B27A")
        self.legendeNoteSucc=self.CAN_Zone.create_text(60, 380,anchor="w",text = "Intervalle de la note suivante" )
        self.rectangleNote=self.CAN_Zone.create_rectangle(10,370,40,390, fill = "#F4D03F")
        self.note=0 #texte dans le canva affichant la note
        self.notePrec=0 #texte dans le canva affichant la note précéente
        self.noteSucc=0 #texte dans le canva affichant la note suivante
        self.frameBouton= tkinter.Frame(fenetre)
        self.frameBouton.config(background="#D9D9D9")
        self.bouton_lancer = tkinter.Button(self.frameBouton, text="Lancer", command=self.estEnPause, background="WHITE", fg="#B38C30") #bouton pour lancer l'accordeur
        self.bouton_lancer.grid(row=1,column=0)
        self.frameBouton.grid(row=3,column=1)
        self.filename="output.wav" #nom du fichier temporaire ou est enregistré le son
        self.p=p
        self.rm=0
        self.fenetre.grid_columnconfigure(0,weight=1)
        self.fenetre.grid_columnconfigure(1,weight=1)
        self.fenetre.grid_columnconfigure(2,weight=1)
        self.fenetre.grid_rowconfigure(0,weight=1)
        self.fenetre.grid_rowconfigure(1,weight=1)
        self.fenetre.grid_rowconfigure(2,weight=1)
        self.fenetre.grid_rowconfigure(3,weight=1)
        self.fenetre.grid_rowconfigure(4,weight=1)
        self.fenetre.grid_rowconfigure(5,weight=1)
        self.frameBouton.grid_columnconfigure(0,weight=2)
        self.frameBouton.grid_columnconfigure(1,weight=1)
        self.frameBouton.grid_columnconfigure(2,weight=2)

    def run(self):
        while not self._stopevent.isSet():
            tab = back.gen_frequences() #création du tableau des fréquences pour détection de la note

            sample_format = pyaudio.paInt16  # 16 bits per sample
            channels = 1
            fs = 44100  # Nombre de samples par seconde
            #instrument cible : clarinette -> dernière octave utilisée : 5ème (2kHz) => Théorème de Shannon : 2*2kHz
            chunk = 2048*2 #enregistrement en morceaux de x samples
            seconds = chunk/fs #analyse sur la durée d'un chunk pour analyser un chunk à la fois


        
            while self.enpause :
                if os.path.exists(self.filename) and self.rm==1:
                    os.remove(self.filename) #supprime le fichier temporaire
                    self.rm=0
                time.sleep(0.5)
                
                
            #Ouverture du micro
            stream = self.p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)

            frames = []

            #Stocker les informations par chunk
            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk)
                frames.append(data)

            #Enregistrer dans le fichier externe
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(self.p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            #Main frequency of a given file
            file_path = "output.wav"
            data, frate  = soundfile.read(file_path, dtype='int16')

            w = np.fft.fft(data)

            freqs = np.fft.fftfreq(len(w))

            #Find the peak in the coefficients -> indice
            idx = np.argmax(np.abs(w))

            freq = freqs[idx]

            freq_in_hertz = abs(freq * frate)
            freq_in_hertz = freq_in_hertz/(4/3) #TODO est ce que c'est mieux ? réduction de 5 demi-tons
            res=back.find_note(tab,freq_in_hertz)
            notePrec = back.find_note(tab, freq_in_hertz/back.coeff_frequences) #nom de la note précédente
            noteSuiv = back.find_note(tab, freq_in_hertz*back.coeff_frequences) #nom de la note suivante
            if(res[0]!='-'):
                self.CAN_Zone.delete(self.CAN_aiguille,self.CAN_norm,self.CAN_Zone_Green,self.CAN_Zone_Red,self.CAN_Zone_Yellow,self.note,self.notePrec,self.noteSucc)#supprimer les formes du canva déjà existantes
                self.debTot=res[2]
                self.finTot=res[3]
                self.finNote=(res[3]+res[1])/2
                self.debNote=(res[2]+res[1])/2
                self.ecart["text"]="Ecart : "+str(round(res[4],2))+" Hz"
                x=int(270+235*math.cos(math.radians(180+((freq_in_hertz*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))#determine la position x de la fin du segment de l'aiguille 
                y=int(270+235*math.sin(math.radians(180+((freq_in_hertz*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))#determine la position y de la fin du segment de l'aiguille 
                self.CAN_Zone_Green = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=(self.finTot*180/(self.finTot-self.debTot))-(self.finNote*180/(self.finTot-self.debTot)), extent =(self.finNote*180/(self.finTot-self.debTot))-(self.debNote*180/(self.finTot-self.debTot)), fill = "#82E0AA",outline="")
                self.CAN_Zone_Red = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=(self.finTot*180/(self.finTot-self.debTot))-(self.finNote*180/(self.finTot-self.debTot))+(self.finNote*180/(self.finTot-self.debTot))-(self.debNote*180/(self.finTot-self.debTot)), extent =(self.debNote*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot)), fill = "#F0B27A",outline="")
                self.CAN_Zone_Yellow = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=0, extent =(self.finTot*180/(self.finTot-self.debTot))-(self.finNote*180/(self.finTot-self.debTot)), fill = "#F4D03F",outline="")
                self.CAN_norm = self.CAN_Zone.create_line(270, 270 , 270 , 20,fill="#8E44AD")
                self.CAN_aiguille = self.CAN_Zone.create_line(270, 270, x , y,fill="#E74C3C",width=2,arrow='last')
                self.note=self.CAN_Zone.create_text(270, 10, text = res[0] )
                self.notePrec=self.CAN_Zone.create_text(20, 290, text = notePrec[0] )
                self.noteSucc=self.CAN_Zone.create_text(520, 290, text = noteSuiv[0] )
            
            

    def estEnPause(self):
        if self.enpause==False :
            self.pause()
        else:
            self.lancer()
    
    def pause(self):
        self.bouton_lancer.config(background="WHITE", fg="#B38C30", text="Lancer")
        self.enpause=True
        self.rm=1
        

    def lancer(self):
        self.bouton_lancer.config(background="#B38C30", fg="WHITE", text="Stop")
        self.enpause=False

    def stop(self):
        self._stopevent.set
    














            


