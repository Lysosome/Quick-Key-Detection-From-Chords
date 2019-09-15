"""
Ben Ma
Python 3.x
"""


#create key of C Major and Minor tables
#then just shift
import caster

noteNums = [('C#', 1), ('D#', 3), ('F#', 6), ('G#', 8), ('A#', 10), ('C', 0), ('D', 2), ('E', 4), ('F', 5), ('G', 7),
            ('A', 9), ('B', 11)]  # have to check the sharps first so it doesn't switch 'C#' into 'w0#'

fullKeyTable = [[[]]] #outer level: major/melodic minor/harmonic minor
#middle level: the twelve "root keys": C, C#, D, D#, etc.
#inner level: all the chords within that root key
fullKeyTable[0][0] = ["C", "Dm", "Em", "F", "G", "G7", "Am", "Bdim"] #major
fullKeyTable.append([["Cm", "Dm", "D#7", "F", "G", "G7", "Adim", "Bdim"]]) #melodic minor... note D#aug converted to D#7 by our casting
fullKeyTable.append([["Cm", "Ddim", "D#7", "Fm", "G", "G7", "G#", "Bdim"]]) #harmonic minor
for k in range(0,len(fullKeyTable)):
    for i in range(1,12):
        curKey = []
        for j in range(0,len(fullKeyTable[k][0])):
            tempChord = caster.makeFlatsSharps(fullKeyTable[k][0][j])
            curKey.append(caster.shiftNumChord(caster.letterChordToNumChord(tempChord, noteNums), i))
        fullKeyTable[k].append(curKey)

with open("key_table_UTF-8.txt", "w") as f:
    for level in fullKeyTable:
        for key in level:
            for note in key:
                note = caster.numChordToLetterChord(note)
                f.write(note+" "),
            f.write("\n")
print("Finished generating key tables")