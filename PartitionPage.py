from distutils import extension
import threading
import pyaudio
import wave
import soundfile
import numpy as np
from back import *
from tkinter import *
import time
from math import *
import os
from midiutil.MidiFile import MIDIFile
from timeit import default_timer as timer
from music21 import converter, instrument
from chrono import * 

def only_numbers(char):
    return char.isdigit()

def titreValide(char):
    #TODO ajouter des caractères interdits si nécessaire
    pattern = "(?=.*:)[^^:]*|\\<>"
    return not(char in pattern)

start = 0
end = 0

class Partition(threading.Thread):

    def __init__(self,fenetre,p):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.enpause=True #variable booleaine pour savoir si il faut stopper ou continuer le programme
        self.fenetre=fenetre #correspond à la fenetre de la page du tunner
        self.label = Label(self.fenetre) #correspond au label qui affiche la note
        self.label["text"]="Partition"
        self.label.config(background="#D9D9D9", font=30)
        self.label.grid(row=0,column=0,sticky='N')
        self.validation = fenetre.register(only_numbers)
        self.validationTitre = fenetre.register(titreValide)
        self.frameTot= Frame(fenetre)
        self.frameTot.config(background="#D9D9D9")
        self.frameParametres= Frame(self.frameTot)
        self.frameParametres.config(background="#D9D9D9")
        self.LabelTitre = Label(self.frameParametres, text="Titre")
        self.LabelTitre.grid(row=0, column=0)
        self.LabelTitre.config(background="#D9D9D9")
        self.ETitre = Entry(self.frameParametres,validate="key", validatecommand=(self.validationTitre, '%S'))
        self.ETitre.grid(row=0, column=1)
        self.erreur = Label(self.frameParametres) #correspond au label qui affiche la note
        self.erreur["text"]=""
        self.erreur.config(background="#D9D9D9",fg="RED")
        self.erreur.grid(row=3, column=1)
        self.LabelTempo = Label(self.frameParametres, text="Tempo")
        self.LabelTempo.grid(row=1, column=0)
        self.LabelTempo.config(background="#D9D9D9")
        self.ETempo = Entry(self.frameParametres,validate="key", validatecommand=(self.validation, '%S'))
        self.ETempo.grid(row=1, column=1)
        self.LabelExtension=Label(self.frameParametres) #correspond au label qui affiche la note
        self.LabelExtension["text"]="Le ou les types de fichier(s) : "
        self.LabelExtension.grid(row=2,column=0)
        self.LabelExtension.config(background="#D9D9D9")
        self.frameCheck= Frame(self.frameParametres)
        self.frameCheck.config(background="#D9D9D9")
        self.extension1 = IntVar()
        self.checkButton1=Checkbutton(self.frameCheck, text="MIDI", variable=self.extension1,onvalue=1, offvalue=0)
        self.extension2 = IntVar()
        self.checkButton2=Checkbutton(self.frameCheck, text="PARTITION", variable=self.extension2,onvalue=1, offvalue=0)
        self.checkButton1.grid(row=0,column=1)
        self.checkButton1.config(background="#D9D9D9")
        self.checkButton2.grid(row=0,column=2)
        self.checkButton2.config(background="#D9D9D9")
        self.frameCheck.grid(row=2,column=1)
        self.frameParametres.grid(row=0,column=0,sticky='NS')
        self.chrono=Chrono(self.frameTot)
        self.frameTot.grid(row=1,column=0,sticky='WENS')
        self.frameBouton= Frame(fenetre)
        self.frameBouton.config(background="#D9D9D9")
        self.bouton_lancer = Button(self.frameBouton, text="Lancer", command=self.lancer,background="WHITE", fg="#B38C30") #bouton pour lancer l'accordeur
        self.bouton_lancer.grid(row=1,column=0)
        self.bouton_stop = Button(self.frameBouton, text="Stop", command=self.pause, background="#B38C30", fg="WHITE")#bouton pour stopper l'accordeur
        self.bouton_stop.grid(row=1,column=2)
        self.vide=Label(self.frameBouton)
        self.vide["text"]= "      "
        self.vide.config(background="#D9D9D9")
        self.vide.grid(row=1,column=1)
        self.frameBouton.grid(row=2,column=0)
        self.p=p
        self.filename="output.wav" #nom du fichier temporaire ou est enregistré le son #TODO nom de fichier fait casser avec celui de tunerpage
        self.rm=0
        self.frameParametres.grid(padx=30, pady=0)
        self.label.grid(padx=0, pady=20)
        self.fenetre.grid_rowconfigure(1,weight=1)
        self.fenetre.grid_rowconfigure(2,weight=1)
        self.fenetre.grid_columnconfigure(0,weight=1)
        self.frameParametres.grid_rowconfigure(0,weight=1)
        self.frameParametres.grid_rowconfigure(1,weight=1)
        self.frameParametres.grid_rowconfigure(2,weight=1)
        self.frameTot.grid_columnconfigure(0,weight=1)
        self.frameTot.grid_columnconfigure(1,weight=1)
        self.frameTot.grid_rowconfigure(0,weight=1)
        self.frameBouton.grid_columnconfigure(0,weight=3)
        self.frameBouton.grid_columnconfigure(1,weight=1)
        self.frameBouton.grid_columnconfigure(2,weight=2)

    def run(self):
        tab = gen_frequences() #création du tableau des fréquences pour détection de la note

        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Nombre de samples par seconde
        #instrument cible : clarinette -> dernière octave utilisée : 5ème (2kHz) => Théorème de Shannon : 2*2kHz
        chunk = 2048*2 #enregistrement en morceaux de x samples
        seconds = chunk/fs #analyse sur la durée d'un chunk pour analyser un chunk à la fois

        while not self._stopevent.isSet():
            while self.enpause:
                if os.path.exists(self.filename) and self.rm==1 :
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
            data_size = len(data)

            w = np.fft.fft(data)

            freqs = np.fft.fftfreq(len(w))

            #Find the peak in the coefficients -> indice
            idx = np.argmax(np.abs(w))

            freq = freqs[idx]

            freq_in_hertz = abs(freq * frate)
            res=find_note(tab,freq_in_hertz)
            tab_MIDI_song.append(find_Midi_Note(res[0]))
        

    def lancer(self):
        if (self.enpause==True):
            self.bouton_lancer.config(background="#B38C30", fg="WHITE")
            self.bouton_stop.config(background="WHITE", fg="#B38C30")
            if(self.ETitre.get()!="." and self.ETitre.get()!=".." and self.ETitre.get()!="" and self.ETempo.get()!="" and (self.extension1.get()==1 or self.extension2.get()==1)):
                duree_noire = 60/int(self.ETempo.get()) #TODO est ce que y en a besoin ici ? je crois que non
                global start #faire de start une variable globale
                start = timer() #clock
                self.erreur["text"]=""
                self.enpause=False
                self.chrono.startChrono()
            else :
                self.erreur["text"]="Erreur du titre ou du tempo ou aucun format séléctionné"

    def pause(self):
        if(self.ETempo.get()!=""):
            duree_noire = 60/int(self.ETempo.get())
            if (self.enpause==False):
                self.enpause=True
                self.rm=1
                global end #faire de end une variable globale
                end = timer() #clock
                duree = end - start
                self.chrono.stopChrono()
                self.chrono.resetChrono()
                self.bouton_lancer.config(background="WHITE", fg="#B38C30")
                self.bouton_stop.config(background="#B38C30", fg="WHITE")
                if(duree < 3):
                    self.erreur["text"]="Durée inférieure à 3 secondes, temps insuffisant"
                    return

                if(len(tab_MIDI_song) !=0):
                    duree_chunk = duree/len(tab_MIDI_song) #durée d'un chunk
                else:
                    self.erreur["text"]="Erreur notes non enregistrées"
                    return

                (tab_coeff_MIDI,tab_notes_MIDI)=arrange_MIDI()
                
                #Création du fichier Midi
                mf = MIDIFile(1) #MidiFile à une portée
                track = 0 #définition de la portée de référence

                time = 0 #temps de départ
                mf.addTrackName(track, time, "Sample Track")
                #mf.addTempo(track, time, int(self.ETempo.get()))
                mf.addTimeSignature(track, time,4,4,60,notes_per_quarter=8)

                channel = 0
                volume = 100

                #mf.addProgramChange(track, channel, time, 72)

                for i in range(len(tab_notes_MIDI)): #Parcours des notes de tab_MIDI_song
                    #mf.addProgramChange(0, i, 0, 72)
                    if(tab_notes_MIDI[i] == "-"): #Si pas de note on laisse un silence
                        time+=(tab_coeff_MIDI[i]*duree_chunk)/duree_noire
                    else: #Sinon on ajoute la note avec une durée de 1
                        pitch = int(tab_notes_MIDI[i]) 
                        duration = (tab_coeff_MIDI[i]*duree_chunk)/duree_noire
                        time+=duration
                        mf.addNote(track, channel, pitch, time, duration, volume)

                #Ecrire sur le fichier MIDI 
                titre = self.ETitre.get()
                with open(titre+".mid", 'wb') as outf: #dans cette version le arrange_MIDI ne casse pas mais ça oui
                    mf.writeFile(outf)  

                mf.close()
        else :
            if (self.enpause==False):
                self.enpause=True


