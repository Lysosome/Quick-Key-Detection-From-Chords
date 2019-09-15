"""
Author: Ben Ma
Python 3.x

This file provides helper functions for the Songwriter utility.

"""

import csv

xIndexFile = "newData\\gram_list_indices.csv"
yIndexFile = "newData\\one_gram_list_indices.csv"

#reads in the X or Y Indices file
#returns a list where the index is the index and the value is the chord progression
def readIndices(data_file):
    ret = []
    with open(data_file, 'r') as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            ret.append(row[0].split(',')[1])
    return ret


#reads in the training examples
def readExamples(data_file):
    x = []
    y = []
    with open(data_file, 'r') as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            x.append(row[0].split(',')[0])
            y.append(row[0].split(',')[1])
    return (x, y)

#splits cadences to list of constituent chords
#e.g. 'A#-F-C#m' to ['A#','F','C#m']
def splitCadence(toSplit):
    return toSplit.split('-')

def secondMax(theList):
    theList.remove(max(theList))
    return max(theList)

def thirdMax(theList):
    theList.remove(max(theList))
    theList.remove(max(theList))
    return max(theList)
