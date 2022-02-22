#Setup de l'application, initialiser les emplacements par défaut d'enregistrement et de musescore
#serial dossier caché pour stocker les informations

import os

file_path = "C:\\Users\\" + os.getlogin() + "\\Downloads\\"
musescore_path = "C:\\Program Files\\MuseScore 3\\bin\\"

fichier = open('../serial/file', 'w+')
fichier.truncate(0) #supprimer le précédent contenu du fichier
fichier.write(file_path) #écrire le nouveau chemin
fichier.close()

musescore = open('../serial/musescore', 'w+')
musescore.truncate(0)
musescore.write(musescore_path)
musescore.close()