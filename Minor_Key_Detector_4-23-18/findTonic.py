"""
Ben Ma
Python 3.x

Defines the findTonicNum and findTonicLet functions

"""

import caster
import copy
import songwriterMethods

#TODO: implement major/minor tiebreakers including counting up total major and minor chords
def findTonicNum(songChords, keyTable): #songChords is a list, keyTable is a list of lists
    # edit songChords to change 7ths to just major
    songChordsNo7 = copy.deepcopy(songChords)
    for i in range(0, len(songChordsNo7)):
        songChordsNo7[i] = songChordsNo7[i].replace("7", "")

    maxKey = 0 #0 thru 11 for C thru B
    maxScore = 0
    #following vars are used as tiebreakers for major/relative minor later
    totalMajors = 0
    totalMinors = 0
    max_I_count = 0
    max_vi_count = 0
    for i in range(0,12): #go thru each of the 12 major keys--example for key of C: C Dm Em F G G7 Am Bdim
        curScore = 0
        current_I_count = 0
        current_vi_count = 0
        key = keyTable[i]
        for chord in songChordsNo7:
            if(i==0 and chord.find('m')==-1):
                totalMajors+=1
            elif(i==0):
                totalMinors+=1
            for j in range(0,len(key)): #go thru each note in the major scale of the key
                note = key[j]
                if chord==note:
                    if (j == 1 or j == 2 or j == 7):
                        curScore+=0.9 #tiebreaker: the ii, iii, and vii are weighted less
                    else:
                        if(j==0):
                            current_I_count+=1
                        elif(j==6):
                            current_vi_count+=1
                        curScore+=1 #if it's a match, add 1 to the "score" of the current key
                    break
        if curScore>maxScore:
            maxScore=curScore
            maxKey = i
            max_I_count = current_I_count
            max_vi_count = current_vi_count
    #now our best-fitting major key is stored in maxKey

    maxKey = "w" + (str)(maxKey)

    # we determine between maxKey and its relative minor
    # naive tiebreaker rules
        # 1. If total Majors or total I's is 0, it's minor
        # likewise, if total minors or total vi's is 0, it's major
        # 2. Otherwise, compare totalMajors+total I's against totalMinors+total vi's
    if(totalMajors==0 or max_I_count==0 or (totalMinors+max_vi_count>totalMajors+max_I_count)):
        maxKey = (caster.shiftNumChord(maxKey, 9)) + "m"

    return maxKey #return key with most matches for the chords in the song

def findTonicLet(songChords, keyTable):
    return caster.numChordToLetterChord(str(findTonicNum(songChords, keyTable)))

def readInFromFile(data_file):
    songList = []  # list of lists
    songNames = []
    count = -1  # counts what inner list we're on
    totalLines = 0
    with open(data_file, 'r') as f:
        curLine = f.readline()
        while (curLine != ""):
            if (curLine != "\n" and curLine.find("| | S O N G M A R K E R | |") == -1):
                songList.append([])
                count += 1
                while (curLine.find("| | S O N G M A R K E R | |") == -1):  # while we're not at the Songmarker
                    lineChords = curLine.split()
                    songList[count].extend(lineChords)
                    totalLines+=1
                    curLine = f.readline()
            # now we've hit a songmarker -- song over
                songNames.append(curLine.replace("| | S O N G M A R K E R | |   ", ""))
            curLine = f.readline()
    return (songList, songNames)

#tester main
if (__name__=="__main__"):
    # global scope variables
    noteNums = [('C#', 1), ('D#', 3), ('F#', 6), ('G#', 8), ('A#', 10), ('C', 0), ('D', 2), ('E', 4), ('F', 5),
                ('G', 7),
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
        while (curLine != ""):
            keyTable.append(curLine.split())
            curLine = f.readline()
    print(keyTable)  # test to make sure we've read table correctly

    # Find song numbers of the songs we chose for "50RandomSongsKeyTesting.txt"

    findSongList = []
    oldTonicList = []
    with open('50RandomSongsKeyTesting_MajorsOnly.txt') as f:
        curLine = f.readline()
        while (curLine != ""):
            if (curLine.find("Calculated Tonic Num") != -1):
                # we're at a song info line
                chord = curLine.split("Calculated Tonic Num: ")[1].split(",")[0]
                song = curLine.split("Song name: ")[1]
                if (song.find("\n") == -1):
                    song += "\n"
                findSongList.append(song)
                oldTonicList.append(chord)
            curLine = f.readline()
    songNumList = []
    data_file = 'chords_uku_english_only_songmarkers.txt'
    (songList, songNames) = readInFromFile(data_file)
    for songName in findSongList:
        songNumList.append(songNames.index(songName))
    counter = 0
    for songNum in songNumList:
        # find tonic chord
        tonicLet = findTonicLet(songList[songNum], keyTable)

        # print all chords in song
        for origChord in songList[songNum]:
            print(origChord, end=' ')
        print("\n" + (str)(counter + 1) + ". Calculated Tonic Num: " + tonicLet + ", Song name:"+ songNames[songNum])
        counter += 1

    """
    #OLD MAIN
    
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
    """