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
from midiutil.MidiFile import MIDIFile #TODO à mettre dans PartitionPage quand ce sera fait

class Tuner(threading.Thread):
    def __init__(self,fenetre):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.enpause=True #variable booleaine pour savoir si il faut stopper ou continuer le programme
        self.fenetre=fenetre #correspond à la fenetre de la page du tunner
        self.label = Label(self.fenetre) #correspond au label qui affiche la note
        self.label["text"]=""
        self.label.config(background="WHITE")
        self.debTot=0 #variable qui contient la fréquence de la note précédente
        self.finTot=0 #variable qui contient la fréquence de la note suivante
        self.finNote=0 #variable qui contient la fréquence de la fin de l'intervalle des fréquences pour la note 
        self.debNote=0 #variable qui contient la fréquence de le début de l'intervalle des fréquences pour la note 
        self.ecart = Label(self.fenetre)#correspond au label qui affiche l'écart entre la fréquence de la note et la fréquence obtenue
        self.ecart["text"]=""
        self.ecart.config(background="WHITE")
        self.label.pack()
        self.ecart.pack()
        self.CAN_Zone = Canvas ( self.fenetre , bg = "white" , height = 350 , width = 1080 ) #canva qui va contenir le compteur
        self.CAN_Zone.pack()
        self.CAN_Zone_Total = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520 , start = 0 , extent = 180 , fill = "#CCD1D1",outline="" )#arc de cercle corresponant à la totalité du compteur
        self.CAN_Zone_Red = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520 , start=0, extent =0, fill = "#F0B27A",outline="")#arc de cercle corresponant à la partie avant l'intervalle de la note
        self.CAN_Zone_Green = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520   , start=0, extent =0, fill = "#82E0AA",outline="")#arc de cercle corresponant à l'intervalle de la note
        self.CAN_Zone_Yellow = self.CAN_Zone.create_arc ( 20 , 20 , 520 , 520  , start=0, extent =0, fill = "#F4D03F",outline="")#arc de cercle corresponant à la partie après l'intervalle de la note
        self.CAN_aiguille =0 #aiguille du compteur
        self.CAN_norm =0 #segment correspondant à la fréquence de la note
        self.note=0 #texte dans le canva affichant la note
        self.notePrec=0 #texte dans le canva affichant la note précéente
        self.noteSucc=0 #texte dans le canva affichant la note suivante
        self.bouton_lancer = Button(fenetre, text="Lancer", command=self.lancer) #bouton pour lancer l'accordeur
        self.bouton_lancer.pack()
        self.bouton_stop = Button(fenetre, text="stop", command=self.pause)#bouton pour stopper l'accordeur
        self.bouton_stop.pack()
        self.filename="output.wav" #nom du fichier temporaire ou est enregistré le son

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
                    os.remove(self.filename) #supprime le fichier temporaire
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
            tab_MIDI_song.append(find_Midi_Note(res[0]))
            #print("code MIDI de ",res,": ",find_Midi_Note(res[0])) #TODO à supprimer : affichage du code midi pour chaque note entendue, ça marche bien
            notePrec = find_note(tab, freq_in_hertz/coeff_frequences) #nom de la note précédente #TODO ? juste limiter à notePrec[0] pour avoir que le nom (le reste sert à rien pour cette utilisation)
            noteSuiv = find_note(tab, freq_in_hertz*coeff_frequences) #nom de la note suivante
            if(res[0]!='-'):
                self.label["text"]="Note : ",res[0]
                self.CAN_Zone.delete(self.CAN_aiguille,self.CAN_norm,self.CAN_Zone_Green,self.CAN_Zone_Red,self.CAN_Zone_Yellow,self.note,self.notePrec,self.noteSucc)#supprimer les formes du canva déjà existantes
                self.debTot=res[2]
                self.finTot=res[3]
                self.finNote=(res[3]+res[1])/2
                self.debNote=(res[2]+res[1])/2
                self.ecart["text"]="Ecart : ",res[4]
                x=int(270+235*cos(radians(180+((freq_in_hertz*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))#determine la position x de la fin du segment de l'aiguille 
                y=int(270+235*sin(radians(180+((freq_in_hertz*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))#determine la position y de la fin du segment de l'aiguille 
                xn=int(270+250*cos(radians(180+((res[1]*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))#determine la position x de la fin du segment de la fréquence de la note
                yn=int(270+250*sin(radians(180+((res[1]*180/(self.finTot-self.debTot))-(self.debTot*180/(self.finTot-self.debTot))))))#determine la position y de la fin du segment de la fréquence de la note
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
        # create your MIDI object
        mf = MIDIFile(1)     # only 1 track
        track = 0   # the only track

        time = 0    # start at the beginning
        mf.addTrackName(track, time, "Sample Track")
        mf.addTempo(track, time, 200)

        # add some notes
        channel = 0
        volume = 100

        for i in range(len(tab_MIDI_song)):
            if(tab_MIDI_song[i] == "-"): #si pas de note on laisse un silence
                time+=1
            else: #sinon on ajoute la note avec une durée de 1
                pitch = int(tab_MIDI_song[i]) 
                time+=1
                duration = 1
                mf.addNote(track, channel, pitch, time, duration, volume)

        # write it to disk
        with open("output.mid", 'wb') as outf: #on écrit dans le fichier MIDI
            mf.writeFile(outf)
        

    def lancer(self):
        self.enpause=False
    














            


