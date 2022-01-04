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

def find_note(frequences, note):
    i = 0
    #note hors du tableau de fréquence mais à un écart faible : on renvoie la note, sinon : return "-"
    if(note<(frequences[0][tab_notes[0]])/coeff_frequences+((frequences[0][tab_notes[0]])-frequences[0][tab_notes[0]]/coeff_frequences)/2): return ("-",0,0,0,0)

    #TODO param crash freq trop petite
    #if(note<frequences[0][tab_notes[0]]) : return ((str(tab_notes[0])+str(0)),frequences[0][tab_notes[0]],round(frequences[0][0]/coeff_frequences,2),round(frequences[0][tab_notes[0]]*coeff_frequences,2),(100 - (frequences[0][tab_notes[0]]*100 / note)))

    if(note>frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences - (frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences - frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]])/2): return ("-",0,0,0,0)
    #TODO param crash freq trop grande
    if(note>frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]) : return ((str(tab_notes[len(tab_notes) - 1])+str(nb_octaves-1)),round(frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]/coeff_frequences,2),round(frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences,2),frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]],(100 - (frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*100 / note)))

    #comparaison du while : entre la première valeur de l'octave (le do) et celle de l'octave suivante (peut importe s'il existe ou non dans le tableau)
    while not(note>=frequences[i][tab_notes[0]] and note<=frequences[i][tab_notes[0]]*2): #trouver la bonne octave
        i = i+1
        #TODO est ce que j'ai vraiment besoin de cette condition ?
        if(i==len(frequences)): #note non présente dans le tableau des fréquences (comparativement au paramètre nombre d'octave)
            return ("-",0,0,0,0)
    #l'octave a été trouvée
    octave = list(frequences[i].values()) #transformer le tableau dict en list de fréquences

    #cas où la fréquence recherchée est entre la dernière valeur d'une octave et la première de l'octave suivante
    if(note>octave[len(tab_notes)-1] + (octave[len(tab_notes)-1]*coeff_frequences - octave[len(tab_notes)-1])/2): return ((str(tab_notes[0])+str(i+1)),frequences[i+1][tab_notes[0]],frequences[i][tab_notes[len(tab_notes) -1]],frequences[i+1][tab_notes[1]],(100 - (frequences[i+1][tab_notes[0]]*100 / note))) 

    #trouver la note jouée
    abs_fctn = lambda octave : abs(octave - note)
    closest_freq = min(octave, key=abs_fctn) #trouver la fréquence la plus proche
    ecart = 100 - (closest_freq*100 / note)
    note_joue = tab_notes[octave.index(closest_freq)]
    if(octave.index(closest_freq)-1 > 0) :
        notePrec=octave[octave.index(closest_freq)-1]
    else:
        notePrec=octave[octave.index(closest_freq)]/coeff_frequences
    if(octave.index(closest_freq)+1 < len(octave)) :
        noteSucc=octave[octave.index(closest_freq)+1]
    else:
        noteSucc=octave[octave.index(closest_freq)]*coeff_frequences
    return ((note_joue + str(i)),closest_freq,notePrec,noteSucc,ecart) #afficher la note jouée et son numéro d'octave
    

