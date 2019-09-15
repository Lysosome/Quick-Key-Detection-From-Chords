"""
Ben Ma
Python 3.x

Prints out first 50 songs with their chords and the calculated tonic
For testing purposes, to see if the tonic num function works well

"""

import caster

def findTonicNum(songChords, keyTable): #songChords is a list, keyTable is a list of lists
    maxKey = 0 #0 thru 11 for C thru B
    maxScore = 0
    for i in range(0,len(keyTable)): #go thru each of the 12 keys--example for key of C: C Dm Em F G G7 Am Bdim
        curScore = 0
        key = keyTable[i]
        for chord in songChords:
            for j in range(0,len(key)): #go thru each note in the major scale of the key
                note = key[j]
                if chord==note:
                    if (j == 1 or j == 2 or j == 7):
                        curScore+=0.9 #tiebreaker: the ii, iii, and vii are weighted less
                    else:
                        curScore+=1 #if it's a match, add 1 to the "score" of the current key
                    break
        if curScore>maxScore:
            maxScore=curScore
            maxKey = i
    return maxKey #return key with most matches for the chords in the song

#global scope variables
noteNums = [('C#', 1), ('D#', 3), ('F#', 6), ('G#', 8), ('A#', 10), ('C', 0), ('D', 2), ('E', 4), ('F', 5), ('G', 7),
            ('A', 9), ('B', 11)]  # have to check the sharps first so it doesn't switch 'C#' into 'w0#'
cadences = []

# read in cadence casting table
with open('cadence_casting_UTF-8.txt', 'r') as f:
    inputs = []
    outputs = []
    exploLine = []
    for line in f:
        exploLine = line.split("\t")
        exploLine[0] = exploLine[0].replace('\xef\xbb\xbf', '')  # clean up special chars
        inputs.append(exploLine[0].replace('\ufeff', '').strip())  # clean up the special chars
        outputs.append(exploLine[1].replace('\n', '').strip())  # clean up special chars
    castingTable = list(zip(inputs, outputs))  # convert casting table to a list of tuples
    print("Opened Cadence Casting Table")
print(castingTable)  # test to make sure we've read in the table correctly

# read in key tables for finding tonic num
keyTable = []
with open('key_table_UTF-8.txt', 'r') as f:
    curLine = f.readline()
    while(curLine!=""):
        keyTable.append(curLine.split())
        curLine = f.readline()
print(keyTable) # test to make sure we've read table correctly

#read in chords from file, song by song
#split is by "  | | S O N G M A R K E R | |", and it starts with lyrics and the songmarker is AFTER each song

with open('chords_uku_english_only_songmarkers.txt', 'r') as f:
    curLine = f.readline()
    counter = 0 #use this to only go thru 50 songs
    while (curLine!="" and counter<50):
        #--STAGE 0: RESET--
        origChords = []
        numChords = []
        tonicNum = 0

        #--STAGE 1: READING SONG--
        if (curLine!="\n"):
            while(curLine.find("| | S O N G M A R K E R | |")==-1): #while we're not at the Songmarker
                lineChords = curLine.split()
                for chord in lineChords:
                    origChords.append(chord)
                curLine = f.readline()
        # now we've hit a songmarker, so let's move on to processing!

        #--STAGE 2: PROCESSING--
        #only process if there actually are chords in origChords
        if(len(origChords)>0):
            #find tonic chord
            tonicNum = findTonicNum(origChords, keyTable)

            #print all chords in song
            for origChord in origChords:
                print(origChord, end=' ')
            tonicLet = caster.numChordToLetterChord("w"+str(tonicNum))
            print("\n"+(str)(counter+1)+". Calculated Tonic Num: " + tonicLet + "\n")
            counter += 1
        curLine = f.readline()
