import music21 as m

us = m.environment.UserSettings()
us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
us['musicxmlPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'

#parsed = m.converter.parse("test.mid")
parsed = m.converter.parse("newfilename.mid")
#parsed = m.converter.parse("clarinet.mid")
#parsed.show("text")

conv_musicxml = m.converter.subConverters.ConverterMusicXML()
scorename = 'test.xml'
filepath = 'C:/Users/leoco/Desktop/all/Cours/L3/MakeSheet/' + scorename
out_filepath = conv_musicxml.write(parsed, 'musicxml', fp=filepath, subformats=['pdf'])