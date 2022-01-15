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
        self.label["text"]="fenetre"
        self.label.config(background="WHITE")
        self.label.pack()
        self.validation = fenetre.register(only_numbers)
        self.validationTitre = fenetre.register(titreValide)
        self.LabelTitre = Label(fenetre, text="Titre")
        self.LabelTitre.pack()
        self.ETitre = Entry(fenetre,validate="key", validatecommand=(self.validationTitre, '%S'))
        self.ETitre.pack()
        self.erreur = Label(self.fenetre) #correspond au label qui affiche la note
        self.erreur["text"]=""
        self.erreur.config(background="WHITE")
        self.erreur.pack()
        self.LabelTempo = Label(fenetre, text="Tempo")
        self.LabelTempo.pack()
        self.ETempo = Entry(fenetre,validate="key", validatecommand=(self.validation, '%S'))
        self.ETempo.pack()
        self.chrono=Chrono(self.fenetre)
        self.bouton_lancer = Button(fenetre, text="Lancer", command=self.lancer) #bouton pour lancer l'accordeur
        self.bouton_lancer.pack()
        self.bouton_stop = Button(fenetre, text="stop", command=self.pause)#bouton pour stopper l'accordeur
        self.bouton_stop.pack()
        self.p=p
        self.filename="output.wav" #nom du fichier temporaire ou est enregistré le son #TODO nom de fichier fait casser avec celui de tunerpage
        self.rm=0

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
                #print(i)
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
            if(self.ETitre.get()!="." and self.ETitre.get()!=".." and self.ETitre.get()!="" and self.ETempo.get()!=""):
                duree_noire = 60/int(self.ETempo.get()) #TODO est ce que y en a besoin ici ? je crois que non
                #print("duree noire : ",duree_noire)
                global start #faire de start une variable globale
                start = timer() #clock
                self.erreur["text"]=""
                self.enpause=False
                self.chrono.startChrono()
            else :
                self.erreur["text"]="Erreur du titre ou du tempo"

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
                if(duree < 3):
                    print("duree inférieure à 3 secondes, temps insuffisant")
                    return

                if(len(tab_MIDI_song) !=0):
                    duree_chunk = duree/len(tab_MIDI_song) #durée d'un chunk
                    #print(duree_chunk)
                else:
                    print("erreur notes non enregistrées")
                    return

                print("tableau midi : ",tab_MIDI_song)
                (tab_coeff_MIDI,tab_notes_MIDI)=arrange_MIDI()
                print(tab_notes_MIDI)
                print(tab_coeff_MIDI)
                
                #Création du fichier Midi
                mf = MIDIFile(1) #MidiFile à une portée
                track = 0 #définition de la portée de référence

                time = 0 #temps de départ
                mf.addTrackName(track, time, "Sample Track")
                mf.addTempo(track, time, int(self.ETempo.get()))

                channel = 0
                volume = 100

                for i in range(len(tab_notes_MIDI)): #Parcours des notes de tab_MIDI_song
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


