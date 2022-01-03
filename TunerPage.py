import threading
import pyaudio
import wave
import soundfile
import numpy as np
from back import *
from tkinter import *
from tkinter import ttk
import time
from math import *
import os

class Tuner(threading.Thread):
    def __init__(self,fenetre):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.enpause=True
        self.fenetre=fenetre
        self.label = Label(self.fenetre)
        self.label["text"]=""
        self.label.config(background="WHITE")
        self.debTot=0
        self.finTot=0
        self.finNote=0
        self.debNote=0
        self.ecart = Label(self.fenetre)
        self.ecart["text"]=""
        self.ecart.config(background="WHITE")
        self.label.pack()
        self.ecart.pack()
        self.CAN_Zone = Canvas ( self.fenetre , bg = "white" , height = 350 , width = 1080 )
        self.CAN_Zone.pack()
        self.CAN_Zone_Total = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520 , start = 0 , extent = 180 , fill = "#CCD1D1",outline="" )
        self.CAN_Zone_Red = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520 , start=0, extent =0, fill = "#F0B27A",outline="")
        self.CAN_Zone_Green = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520   , start=0, extent =0, fill = "#82E0AA",outline="")
        self.CAN_Zone_Yellow = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=0, extent =0, fill = "#F4D03F",outline="")
        self.CAN_aiguille =0
        self.CAN_norm =0
        self.note=0
        self.notePrec=0
        self.noteSucc=0
        self.bouton_lancer = Button(fenetre, text="Lancer", command=self.lancer)
        self.bouton_lancer.pack()
        self.bouton_stop = Button(fenetre, text="stop", command=self.pause)
        self.bouton_stop.pack()
        self.filename="output.wav"

    def run(self):
        tab = gen_frequences() #création du tableau des fréquences pour détection de la note

        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Nombre de samples par seconde
        #instrument cible : clarinette -> dernière octave utilisée : 5ème (2kHz) => Théorème de Shannon : 2*2kHz
        chunk = 2048*2 #enregistrement en morceaux de x samples
        seconds = chunk/fs #analyse sur la durée d'un chunk pour analyser un chunk à la fois

        p = pyaudio.PyAudio() #Instanciation de PyAudio

        while not self._stopevent.isSet():
            while self.enpause:
                if os.path.exists(self.filename):
                    os.remove(self.filename)
                time.sleep(0.5)
                
            #Ouverture du micro
            stream = p.open(format=sample_format,
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
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            #Main frequency of a given file
            file_path = "output.wav"
            data, frate  = soundfile.read(file_path, dtype='int16')
            data_size = len(data)

            w = np.fft.fft(data)

            freqs = np.fft.fftfreq(len(w))

            #Find the peak in the coefficients -> indice
            idx = np.argmax(np.abs(w))

            freq = freqs[idx]

            freq_in_hertz = abs(freq * frate)
            res=find_note(tab,freq_in_hertz)
            notePrec = find_note(tab, freq_in_hertz/coeff_frequences) #nom de la note précédente #TODO ? juste limiter à notePrec[0] pour avoir que le nom (le reste sert à rien pour cette utilisation)
            noteSuiv = find_note(tab, freq_in_hertz*coeff_frequences) #nom de la note suivante
            #TODO à supprimer après les tests
            if(notePrec[0] != "-"):
                print(notePrec[0])
            if(res[0]!='-'):
                self.label["text"]="Note : ",res[0]
                self.CAN_Zone.delete(self.CAN_aiguille,self.CAN_norm,self.CAN_Zone_Green,self.CAN_Zone_Red,self.CAN_Zone_Yellow,self.note,self.notePrec,self.noteSucc)
                self.debTot=res[2]
                self.finTot=res[3]
                self.finNote=(res[3]+res[1])/2
                self.debNote=(res[2]+res[1])/2
                self.ecart["text"]="Ecart : ",res[4]
                x=int(270+235*cos(radians(180+((freq_in_hertz*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))
                y=int(270+235*sin(radians(180+((freq_in_hertz*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))
                xn=int(270+250*cos(radians(180+((res[1]*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))
                yn=int(270+250*sin(radians(180+((res[1]*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))
                self.CAN_Zone_Green = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=(self.finTot*180/(self.finTot-self.debTot))-(self.finNote*180/(self.finTot-self.debTot)), extent =(self.finNote*180/(self.finTot-self.debTot))-(self.debNote*180/(self.finTot-self.debTot)), fill = "#82E0AA",outline="")
                self.CAN_Zone_Red = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=(self.finTot*180/(self.finTot-self.debTot))-(self.finNote*180/(self.finTot-self.debTot))+(self.finNote*180/(self.finTot-self.debTot))-(self.debNote*180/(self.finTot-self.debTot)), extent =(self.debNote*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot)), fill = "#F0B27A",outline="")
                self.CAN_Zone_Yellow = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=0, extent =(self.finTot*180/(self.finTot-self.debTot))-(self.finNote*180/(self.finTot-self.debTot)), fill = "#F4D03F",outline="")
                self.CAN_norm = self.CAN_Zone.create_line(270, 270 , xn , yn,fill="#8E44AD")
                self.CAN_aiguille = self.CAN_Zone.create_line(270, 270, x , y,fill="#E74C3C",width=2,arrow='last')
                self.note=self.CAN_Zone.create_text(270, 10, text = res[0] )
                self.notePrec=self.CAN_Zone.create_text(20, 290, text = notePrec[0] )
                self.noteSucc=self.CAN_Zone.create_text(520, 290, text = noteSuiv[0] )
            
            

    def pause(self):
        self.enpause=True
        

    def lancer(self):
        self.enpause=False
    














            


