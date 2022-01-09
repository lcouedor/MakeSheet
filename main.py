#from os import close
import pyaudio
import wave
import soundfile
import numpy as np

coeff_frequences = 233.08/220.0
tab_notes = ["Do", "Do#", "Re", "Mib", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "Sib", "Si"]

nb_octaves = 7
note_init = (32.7/coeff_frequences)
ecart = 0 #variable pour donner en % l'écart à la fréquence de la note la plus proche

def gen_octave(base_note):
    tab_octave = dict()
    for i in range(len(tab_notes)):
        base_note = round(base_note*coeff_frequences,2)
        #base_note = base_note*coeff_frequences
        tab_octave[tab_notes[i]] = base_note
    return tab_octave

def gen_frequences():
    base_note = note_init
    tab_frequences = [0 for i in range(nb_octaves)]
    for i in range(nb_octaves):
        tab_frequences[i] = gen_octave(base_note)
        base_note = tab_frequences[i][tab_notes[len(tab_notes) - 1]]
    return tab_frequences

def aff(tab):
    for i in range(len(tab)):
        print("octave ",i," : ",tab[i])

def find_Midi_Note(note): #trouver le code midi d'une note à partir de son nom
    if(note=="-"): #cas ou aucune note n'est entendue, pas de code
        return "-"
    else:
        octave = note[-1] #numéro d'octave
        note = note.replace(octave,"") #nom de la note sans son octave
        return tab_notes.index(note) + 24 + (int(octave)-1) * 12 #index de la note dans le tableau + 24 (tableau midi commençant à octave -1, nous à octave 1) + 12 (nb notes) * nb octaves - 1


def find_note(frequences, note):
    i = 0

    #note hors du tableau de fréquence mais à un écart faible : on renvoie la note, sinon : return "-"
    if(note<(frequences[0][tab_notes[0]])/coeff_frequences+((frequences[0][tab_notes[0]])-frequences[0][tab_notes[0]]/coeff_frequences)/2): return "-"
    if(note<frequences[0][tab_notes[0]]) : return (str(tab_notes[0])+str(0))

    if(note>frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences - (frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences - frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]])/2): return "-"
    if(note>frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]) : return (str(tab_notes[len(tab_notes) - 1])+str(nb_octaves-1))

    #comparaison du while : entre la première valeur de l'octave (le do) et celle de l'octave suivante (peut importe s'il existe ou non dans le tableau)
    while not(note>=frequences[i][tab_notes[0]] and note<=frequences[i][tab_notes[0]]*2): #trouver la bonne octave
        i = i+1
        #TODO est ce que j'ai vraiment besoin de cette condition ?
        if(i==len(frequences)): #note non présente dans le tableau des fréquences (comparativement au paramètre nombre d'octave)
            return 0
    #l'octave a été trouvée
    octave = list(frequences[i].values()) #transformer le tableau dict en list de fréquences

    #cas où la fréquence recherchée est entre la dernière valeur d'une octave et la première de l'octave suivante
    if(note>octave[len(tab_notes)-1] + (octave[len(tab_notes)-1]*coeff_frequences - octave[len(tab_notes)-1])/2): return (str(tab_notes[0])+str(i+1)) 

    #trouver la note jouée
    abs_fctn = lambda octave : abs(octave - note)
    closest_freq = min(octave, key=abs_fctn) #trouver la fréquence la plus proche
    ecart = 100 - (closest_freq*100 / note)
    note_joue = tab_notes[octave.index(closest_freq)]

    return note_joue + str(i) #afficher la note jouée et son numéro d'octave

tab = gen_frequences() #création du tableau des fréquences pour détection de la note

sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Nombre de samples par seconde
#instrument cible : clarinette -> dernière octave utilisée : 5ème (2kHz) => Théorème de Shannon : 2*2kHz
chunk = 2048*2 #enregistrement en morceaux de x samples
seconds = chunk/fs #analyse sur la durée d'un chunk pour analyser un chunk à la fois
filename = "output.wav"

p = pyaudio.PyAudio() #Instanciation de PyAudio

#print(find_Midi_Note("Fa#5"))

"""
while True:

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

    #print(freq_in_hertz)
    print(find_note(tab,freq_in_hertz))


#TODO quand on aura une interface graphique : bouton pour lancer et terminer le record : 
#quand record terminé, les analyses de frequences sont finies, on suppr le fichier output qui servait à trouver la freq
"""
