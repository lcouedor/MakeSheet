import threading
import pyaudio
import wave
import soundfile
import numpy as np
from main_ import *
from tkinter import *
import time

class Affiche2(threading.Thread):
    def __init__(self,fenetre):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.enpause=True
        self.fenetre=fenetre
        self.label = Label(self.fenetre)
        self.label["text"]=""
        self.label.pack()
    def run(self):
        tab = gen_frequences() #création du tableau des fréquences pour détection de la note
        #print(find_note(tab,64))
        #TODO même chose que le précédent TODO, mais version entre octaves
        #exemple: pour 64Hz, il return Si0 au lieu de Do1

        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Nombre de samples par seconde
        #TODO ajuster la taille de chunk -> théorème de shannon ?
        chunk = 2048*2 #enregistrement en morceaux de x samples
        seconds = chunk/fs #analyse sur la durée d'un chunk pour analyser un chunk à la fois
        filename = "output.wav"

        p = pyaudio.PyAudio() #Instanciation de PyAudio

        while not self._stopevent.isSet():
            while self.enpause:
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
            #TODO supprimer le fichier output à la fin du programme
            wf = wave.open(filename, 'wb')
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

            self.label["text"]=find_note(tab,freq_in_hertz)
            

    def pause(self):
        self.enpause=True

    def lancer(self):
        self.enpause=False



fenetre = Tk()
c = Affiche2(fenetre)
bouton_lancer = Button(fenetre, text="Lancer", command=c.lancer)
bouton_lancer.pack()
bouton_stop = Button(fenetre, text="stop", command=c.pause)
bouton_stop.pack()
c.start()
fenetre.mainloop()
            

