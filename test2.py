from music21 import converter,instrument
s = converter.parse('test.mid')

for p in s.parts:
    p.insert(0, instrument.Violin())

s.write('midi', 'newfilename.mid')