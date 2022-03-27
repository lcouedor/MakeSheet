import threading
import pyaudio
import wave
import soundfile
import numpy as np
import tkinter
import time
import os
from midiutil.MidiFile import MIDIFile
from timeit import default_timer as timer
from music21 import *
import math

import back
from chrono import Chrono

#Fonction de vérification pour savoir si le paramètre est chiffre ou pas
def only_numbers(char):
    return char.isdigit()

#Fonction de vérification pour savoir si le paramètre n'est pas un caractère spécial
def titreValide(char):
    pattern = "(?=.*:)[^^:]*|\\<>"
    return not(char in pattern)


start = 0
end = 0

class Partition(threading.Thread):

    def __init__(self,fenetre,p):

        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.enpause=True #variable booleaine pour savoir si il faut stopper ou continuer le programme
        self.fenetre=fenetre #correspond à la fenetre de la page de la partition
        self.label = tkinter.Label(self.fenetre) #correspond au titre de la page
        self.label["text"]="Partition"
        self.label.config(background="#D9D9D9", font=30)
        self.label.grid(row=0,column=0,sticky='N')
        self.validation = fenetre.register(only_numbers)
        self.validationTitre = fenetre.register(titreValide)
        self.frameTot= tkinter.Frame(fenetre)
        self.frameTot.config(background="#D9D9D9")
        #Initialisation de la zone de formulaire
        self.frameParametres= tkinter.Frame(self.frameTot)
        self.frameParametres.config(background="#D9D9D9")
        self.LabelTitre = tkinter.Label(self.frameParametres, text="Titre")
        self.LabelTitre.grid(row=0, column=0)
        self.LabelTitre.config(background="#D9D9D9")
        self.ETitre = tkinter.Entry(self.frameParametres,validate="key", validatecommand=(self.validationTitre, '%S'))
        self.ETitre.grid(row=0, column=1)
        self.erreur = tkinter.Label(self.frameParametres) 
        self.erreur["text"]=""
        self.erreur.config(background="#D9D9D9",fg="RED")
        self.erreur.grid(row=5, column=1)
        self.LabelTempo = tkinter.Label(self.frameParametres, text="Tempo")
        self.LabelTempo.grid(row=1, column=0)
        self.LabelTempo.config(background="#D9D9D9")
        self.ETempo = tkinter.Entry(self.frameParametres,validate="key", validatecommand=(self.validation, '%S'))
        self.ETempo.grid(row=1, column=1)
        self.LabelNumerateur = tkinter.Label(self.frameParametres, text="Numérateur")
        self.LabelNumerateur.grid(row=2, column=0)
        self.LabelNumerateur.config(background="#D9D9D9")
        self.ENumerateur = tkinter.Entry(self.frameParametres,validate="key", validatecommand=(self.validation, '%S'))
        self.ENumerateur.grid(row=2, column=1)
        self.LabelDenominateur = tkinter.Label(self.frameParametres, text="Dénominateur")
        self.LabelDenominateur.grid(row=3, column=0)
        self.LabelDenominateur.config(background="#D9D9D9")
        self.EDenominateur = tkinter.Entry(self.frameParametres,validate="key", validatecommand=(self.validation, '%S'))
        self.EDenominateur.grid(row=3, column=1)
        self.LabelExtension=tkinter.Label(self.frameParametres) 
        self.LabelExtension["text"]="Le ou les types de fichier(s) : "
        self.LabelExtension.grid(row=4,column=0)
        self.LabelExtension.config(background="#D9D9D9")
        #Initialisation de la zone de checkBox
        self.frameCheck= tkinter.Frame(self.frameParametres)
        self.frameCheck.config(background="#D9D9D9")
        self.extension1 = tkinter.IntVar()
        self.checkButton1=tkinter.Checkbutton(self.frameCheck, text="MIDI", variable=self.extension1,onvalue=1, offvalue=0)
        self.extension2 = tkinter.IntVar()
        self.checkButton2=tkinter.Checkbutton(self.frameCheck, text="PARTITION", variable=self.extension2,onvalue=1, offvalue=0)
        self.checkButton1.grid(row=0,column=1)
        self.checkButton1.config(background="#D9D9D9")
        self.checkButton2.grid(row=0,column=2)
        self.checkButton2.config(background="#D9D9D9")
        self.frameCheck.grid(row=4,column=1)
        self.frameParametres.grid(row=0,column=0,sticky='NS')
        self.chrono=Chrono(self.frameTot)
        self.frameTot.grid(row=1,column=0,sticky='WENS')
        #Initialisation de la zone de bouton
        self.frameBouton= tkinter.Frame(fenetre)
        self.frameBouton.config(background="#D9D9D9")
        self.bouton_lancer = tkinter.Button(self.frameBouton, text="Lancer", command=self.estEnPause,background="WHITE", fg="#B38C30") #bouton pour lancer l'accordeur
        self.bouton_lancer.grid(row=1,column=0)
        self.frameBouton.grid(row=2,column=0)
        self.p=p
        self.filename="output1.wav"
        self.rm=0
        #Mise en page 
        self.frameParametres.grid(padx=30, pady=0)
        self.label.grid(padx=0, pady=20)
        self.fenetre.grid_rowconfigure(1,weight=1)
        self.fenetre.grid_rowconfigure(2,weight=1)
        self.fenetre.grid_columnconfigure(0,weight=1)
        self.frameParametres.grid_rowconfigure(0,weight=1)
        self.frameParametres.grid_rowconfigure(1,weight=1)
        self.frameParametres.grid_rowconfigure(2,weight=1)
        self.frameParametres.grid_rowconfigure(3,weight=1)
        self.frameParametres.grid_rowconfigure(4,weight=1)
        self.frameTot.grid_columnconfigure(0,weight=1)
        self.frameTot.grid_columnconfigure(1,weight=1)
        self.frameTot.grid_rowconfigure(0,weight=1)
        self.frameBouton.grid_columnconfigure(0,weight=3)
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

            #Ouverture du micro
            stream = self.p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)

            while self.enpause:
                if os.path.exists(self.filename) and self.rm==1 :
                    os.remove(self.filename) #supprime le fichier temporaire
                    self.rm=0
                time.sleep(0.5)

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
            file_path = "output1.wav"
            data, frate  = soundfile.read(file_path, dtype='int16')

            w = np.fft.fft(data)

            freqs = np.fft.fftfreq(len(w))

            #Find the peak in the coefficients -> indice
            idx = np.argmax(np.abs(w))

            freq = freqs[idx]

            freq_in_hertz = abs(freq * frate)
            #freq_in_hertz = freq_in_hertz/(4/3) #est ce que c'est mieux ? réduction de 5 demi-tons
            res=back.find_note(tab,freq_in_hertz)
            back.tab_MIDI_song.append(back.find_Midi_Note(res[0]))
    
    def estEnPause(self):
        if self.enpause==False :
            self.pause()
        else:
            self.lancer()

    def lancer(self):
        if (self.enpause==True):
            #Mise en place de différents teste validant ou nom les informations données
            if(self.ETitre.get()!="." and self.ETitre.get()!=".." and self.ETitre.get()!="" ):
                if (self.ETempo.get()!="" ):
                    if(self.ENumerateur.get()!="") :
                        if(self.EDenominateur.get()=="1" or self.EDenominateur.get()=="2" or self.EDenominateur.get()=="4" or self.EDenominateur.get()=="8" or self.EDenominateur.get()=="16" or self.EDenominateur.get()=="32") :
                            if (self.extension1.get()==1 or self.extension2.get()==1) :
                                global start #faire de start une variable globale
                                start = timer() #clock
                                self.erreur["text"]=""
                                self.enpause=False
                                self.bouton_lancer.config(background="#B38C30", fg="WHITE", text="Stop")
                                self.chrono.startChrono()
                            else :
                                self.erreur["text"]="Erreur : le format est manquant"
                        else:
                            self.erreur["text"]="Erreur : le dénominateur est manquant, il doit être 1, 2, 4, 8, 16 ou 32"
                    else:
                        self.erreur["text"]="Erreur : le numérateur est manquant"
                else:
                    self.erreur["text"]="Erreur : le tempo est manquant"
            else :
                self.erreur["text"]="Erreur : le titre est manquant"

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
                self.bouton_lancer.config(background="WHITE", fg="#B38C30", text="Lancer")
                if(duree < 3):
                    self.erreur["text"]="Erreur : la durée inférieure à 3 secondes, temps insuffisant"
                    return

                if(len(back.tab_MIDI_song) !=0):
                    duree_chunk = duree/len(back.tab_MIDI_song) #durée d'un chunk
                else:
                    self.erreur["text"]="Erreur notes non enregistrées"
                    return

                tab_coeff_MIDI,tab_notes_MIDI=back.arrange_MIDI()
                
                #Création du fichier Midi
                mf = MIDIFile(1) #MidiFile à une portée
                track = 0 #définition de la portée de référence
                time = 0 #temps de départ
                mf.addTrackName(track, time, self.ETitre.get())
                mf.addTempo(track, time, int(self.ETempo.get()))
                mf.addTimeSignature(track, time,int(self.ENumerateur.get()),round(math.sqrt(int(self.EDenominateur.get()))),24,notes_per_quarter=8)

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
                with open(titre+".mid", 'wb') as outf:
                    mf.writeFile(outf)  

                mf.close()

                musescore = open('serial/musescore', 'r')
                cheminMusescore = str(musescore.read())+'MuseScore3.exe'
                musescore.close()

                fichier = open('serial/file', 'r')
                cheminFichier = str(fichier.read())
                fichier.close()

                if(self.extension2.get()==1): #Partition cochée, on la créée et on supprime le fichier temporaire une fois fini

                    us = environment.UserSettings()
                    us['musescoreDirectPNGPath'] = cheminMusescore
                    us['musicxmlPath'] = cheminMusescore

                    parsed = converter.parse(titre+".mid")
                    conv_musicxml = converter.subConverters.ConverterMusicXML()
                    scorename = titre+'.xml'
                    filepath = scorename
                    conv_musicxml.write(parsed, 'musicxml', fp=filepath, subformats=['pdf'])
                    supprime = False
                    while(not(supprime)):
                        if (os.path.exists(titre +'.musicxml')):
                            supprime = True
                            os.remove(titre +'.musicxml')

                    if(os.path.exists(cheminFichier+titre+".pdf")):
                        os.remove(cheminFichier+titre+".pdf")

                    if(os.path.exists(cheminFichier+titre+".mid")):
                        os.remove(cheminFichier+titre+".mid")

                    os.rename(os.getcwd()+"/"+titre+".pdf", cheminFichier+titre+".pdf")

                if(self.extension1.get()==0): #Pas de fichier MIDI, on le supprime une fois la partition créée
                    supprime = False
                    while(not(supprime)):
                        if (os.path.exists(cheminFichier + titre +'.pdf') and os.path.exists(titre +'.mid')):
                            supprime = True
                            os.remove(titre +'.mid')

                if(self.extension1.get()==1):
                    move = False
                    while(not(move)):
                        if (os.path.exists(titre +'.mid')):
                            move = True
                            os.rename(os.getcwd()+"/"+titre+".mid", cheminFichier+titre+".mid")


        else :
            if (self.enpause==False):
                self.enpause=True
    

    def stop(self):
        self._stopevent.set

