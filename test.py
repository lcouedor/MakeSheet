import music21 as m

m.environment.set('musescoreDirectPNGPath', 'C:\Program Files\MuseScore 3')
m.environment.UserSettings()['lilypondPath'] = 'C:\Program Files (x86)\LilyPond' #TODO vérifier dans ce dossier
m.environment.UserSettings()['musicxmlPath'] = 'C:\Program Files\MuseScore 3'
#print(m.environment.UserSettings()['musescoreDirectPNGPath'])
#print(m.environment.UserSettings()['lilypondPath'])
#print(m.environment.UserSettings()['musicxmlPath'])

#print(m.environment.UserSettings()['lilypondPath'])
#m.converter.parse('Itsumo_nando_demo_-_piano.mid').show('musicxml.png')
#parsed = m.converter.parse(r'Itsumo_nando_demo_-_piano.mid')
parsed = m.converter.parse('Itsumo_nando_demo_-_piano.mid')
#parsed.show('text') #solid banana out of 10
#parsed.show('lily.pdf')
#parsed.show('musicxml.png')
#parsed.show('musicxml.png')