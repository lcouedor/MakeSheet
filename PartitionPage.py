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
from midiutil.MidiFile import MIDIFile, TimeSignature #TODO à mettre dans PartitionPage quand ce sera 
from timeit import default_timer as timer

def only_numbers(char):
    return char.isdigit()

def titreValide(char):
    #TODO faire test de la longueur du titre, titre entier différents de . ou .. 
    test = True
    if(char=="<" or char==">" or char==":" or char=='"' or char=="/" or char=="\\" or char=="|" or char=="?" or char=="*") :
        test=False
    return test

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
        self.bouton_lancer = Button(fenetre, text="Lancer", command=self.lancer) #bouton pour lancer l'accordeur
        self.bouton_lancer.pack()
        self.bouton_stop = Button(fenetre, text="stop", command=self.pause)#bouton pour stopper l'accordeur
        self.bouton_stop.pack()
        self.p=p
        self.filename="output2.wav" #nom du fichier temporaire ou est enregistré le son #TODO nom de fichier fait casser avec celui de tunerpage
    

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
                print(i)
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
            file_path = "output2.wav"
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
                duree_noire = 60/int(self.ETempo.get())
                print("duree noire : ",duree_noire)
                global start #faire de start une variable globale
                start = timer() #clock
                self.erreur["text"]=""
                self.enpause=False
            else :
                self.erreur["text"]="Erreur du titre ou du tempo"

    def pause(self):
        if (self.enpause==False):
            global end #faire de end une variable globale
            end = timer() #clock
            duree = end - start
            duree_chunk = duree/len(tab_MIDI_song) #durée d'un chunk
            print(tab_MIDI_song)
            print("taille :",len(tab_MIDI_song))
            print(duree_chunk)
            self.enpause=True
            # create your MIDI object
            mf = MIDIFile(1)     # only 1 track
            track = 0   # the only track

            time = 0    # start at the beginning
            mf.addTrackName(track, time, "Sample Track")
            mf.addTempo(track, time, int(self.ETempo.get()))

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
            titre = self.ETitre.get()
            with open(titre+".mid", 'wb') as outf: #on écrit dans le fichier MIDI
                mf.writeFile(outf)
        
    



