coeff_frequences = 233.08/220.0 #coefficient multiplicateur pour tableau de fréquences
tab_notes = ["Do", "Do#", "Re", "Mib", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "Sib", "Si"] #tableau des notes
tab_MIDI_song = [] #tableau de tous les codes midi

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
        return tab_notes.index(note) + 24 + (int(octave)) * 12 #index de la note dans le tableau + 24 (tableau midi commençant à octave -1, nous à octave 1) + 12 (nb notes) * nb octaves - 1

def arrange_MIDI(): #remplir les tableaux tab_notes_MIDI et tab_coeff_MIDI
    #TODO optimiser la fonction. Avec les noms des variables c'est n'importe quoi

    newTab_coeff_MIDI = []
    newTab_notes_MIDI = []

    max = len(tab_MIDI_song) #taille du tableau des notes MIDI
    if(max > 0): #ajout de la premiere note si elle existe
        newTab_notes_MIDI.append(tab_MIDI_song[0])
        newTab_coeff_MIDI.append(1)
    else: return #sinon tableau vide on return

    #on remplit les tableaux de notes et de coefficients
    for i in range (max-1): #parcours des valeurs du tableau MIDI -1 pour éviter le out of bounds
        if(tab_MIDI_song[i] == tab_MIDI_song[i+1]): #si deux caracteres consécutifs identiques on incrémente le coeff
            newTab_coeff_MIDI[len(newTab_coeff_MIDI)-1] += 1
        else: #sinon on ajoute la note qui n'y est pas et on lui créé un coeff à 1
            newTab_notes_MIDI.append(tab_MIDI_song[i+1])
            newTab_coeff_MIDI.append(1)

    #on évite les notes parasytes en supprimant ce qui n'apparait que sur un seul chunk
    new2Tab_coeff_MIDI = []
    new2Tab_notes_MIDI = []
    for i in range (len(newTab_coeff_MIDI)):
        if(newTab_coeff_MIDI[i] > 1):
            new2Tab_coeff_MIDI.append(newTab_coeff_MIDI[i])
            new2Tab_notes_MIDI.append(newTab_notes_MIDI[i])

    #On concatène à nouveau dans le cas ou un note parasyte était venue couper la série de notes
    new3Tab_coeff_MIDI = []
    new3Tab_notes_MIDI = []

    max = len(new2Tab_notes_MIDI) #taille du tableau des notes MIDI
    if(max > 0): #ajout de la premiere note si elle existe
        new3Tab_notes_MIDI.append(new2Tab_notes_MIDI[0])
        new3Tab_coeff_MIDI.append(new2Tab_coeff_MIDI[0])
    else: return #sinon tableau vide on return

    #on remplit les tableaux de notes et de coefficients
    for i in range (max-1): #parcours des valeurs du tableau MIDI -1 pour éviter le out of bounds
        if(new2Tab_notes_MIDI[i] == new2Tab_notes_MIDI[i+1]): #si deux caracteres consécutifs identiques on incrémente le coeff
            new3Tab_coeff_MIDI[len(new3Tab_coeff_MIDI)-1] += new2Tab_coeff_MIDI[i+1]
        else: #sinon on ajoute la note qui n'y est pas et on lui créé un coeff à 1
            new3Tab_notes_MIDI.append(new2Tab_notes_MIDI[i+1])
            new3Tab_coeff_MIDI.append(new2Tab_coeff_MIDI[i+1])

    #si il y a du silence au début : le supprime
    if(new3Tab_notes_MIDI[0] == "-"):
        new3Tab_notes_MIDI.pop(0)
        new3Tab_coeff_MIDI.pop(0)

    #mettre les tableaux temporaires dans les variables utilisées ailleurs
    tab_notes_MIDI = new3Tab_notes_MIDI
    tab_coeff_MIDI = new3Tab_coeff_MIDI
    return (tab_coeff_MIDI,tab_notes_MIDI)

def find_note(frequences, note):
    i = 0
    #note hors du tableau de fréquence mais à un écart faible : on renvoie la note, sinon : return "-"
    if(note<(frequences[0][tab_notes[0]])/coeff_frequences+((frequences[0][tab_notes[0]])-frequences[0][tab_notes[0]]/coeff_frequences)/2): return ("-",0,0,0,0)

    #TODO param crash freq trop petite
    if(note<frequences[0][tab_notes[0]]) : return ((str(tab_notes[0])+str(0)),frequences[0][tab_notes[0]],round(frequences[0][tab_notes[0]]/coeff_frequences,2),round(frequences[0][tab_notes[0]]*coeff_frequences,2),(100 - (frequences[0][tab_notes[0]]*100 / note)))

    if(note>frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences - (frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences - frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]])/2): return ("-",0,0,0,0)
    #TODO param crash freq trop grande
    if(note>frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]) : return ((str(tab_notes[len(tab_notes) - 1])+str(nb_octaves-1)),frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]],round(frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]/coeff_frequences,2),round(frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*coeff_frequences,2),(100 - (frequences[nb_octaves-1][tab_notes[len(tab_notes) -1]]*100 / note)))

    #comparaison du while : entre la premiere valeur de l'octave (le do) et celle de l'octave suivante (peut importe s'il existe ou non dans le tableau)
    while not(note>=frequences[i][tab_notes[0]] and note<=frequences[i][tab_notes[0]]*2): #trouver la bonne octave
        i = i+1
        #TODO est ce que j'ai vraiment besoin de cette condition ?
        if(i==len(frequences)): #note non présente dans le tableau des fréquences (comparativement au parametre nombre d'octave)
            return ("-",0,0,0,0)
    #l'octave a été trouvée
    octave = list(frequences[i].values()) #transformer le tableau dict en list de fréquences

    #cas où la fréquence recherchée est entre la derniere valeur d'une octave et la premiere de l'octave suivante
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
    

