'''
Team Member #1: Maxwell Sherman
Team Member #2: N/A
Zagmail address for team member 1: msherman3@zagmail.gonzaga.edu
Test 3C: This program implements a CYK parser
Usage: python cyk.py cfg1.txt strng1.txt (or any other cfg/strng files)
Due: 2018-12-14 18:00 PDT
'''

import csv
import sys

def main(): # TODO: if the user enters something small like 1 word sentence
    grammarDict = getGrammar()
    for line in grammarDict:
        print line
    print
    sentence = getSentence()
    #sentence = ["a"]
    print sentence
    print
    n = len(sentence) # length of sentence, size of matrix
    
    cykMatrix = [[0 for word in sentence] for word in sentence] # make nxn array
    cykMatrix = removeTriangle(cykMatrix, n) # put null characters where there shouldn't be anything
    
    cykMatrix = fillMatrix(cykMatrix, n, sentence, grammarDict)
    for line in cykMatrix:
        print line
    
    # if "S" in cykMatrix[n-1][0] then yes, else no

def getGrammar():
    grammarDict = []
    with open(sys.argv[1], mode="r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if len(row) == 2: # terminal
                grammarDict.append((row[0], row[1]))
            elif len(row) == 3: # variable
                grammarDict.append((row[0], row[1], row[2]))
    return grammarDict

def getSentence():
    with open(sys.argv[2], mode="r") as infile:
        sentence = infile.readline()
    return sentence.split()

def removeTriangle(cykMatrix, n):
    for i in range(1, n):
        for j in range(n-i, n):
            cykMatrix[i][j] = None
    return cykMatrix

def fillMatrix(cykMatrix, n, sentence, grammarDict):
    for i in range(n):
        if i == 0: #TODO generalize
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if sentence[j] == rule[1]:
                        cykMatrix[i][j].append(rule[0])
        '''elif i == 1:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if sentence[j] == rule[1]:
                        cykMatrix[i][j].append(rule[0])'''
    return cykMatrix

main()
