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
    
    outputValue = False
    for value in cykMatrix[n-1][0]:
        if value == "S":
            outputValue = True
    
    if outputValue:
        print("Yes")
    else:
        print("No")

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
    for i in range(n): # i and j represent the coordinates of the box in the matrix
        if i == 0:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if len(rule) == 2: # looking for terminals
                        if sentence[j] == rule[1]:
                            cykMatrix[i][j].append(rule[0])
        elif i == 1:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if len(rule) == 3: # looking for variables
                        for k in range(len(cykMatrix[i-1][j])): # k and j are used to iterate over each value in the box
                            for l in range(len(cykMatrix[i-1][j+1])):
                                if cykMatrix[i-1][j][k] == rule[1] and cykMatrix[i-1][j+1][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
        elif i > 1:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if len(rule) == 3: # looking for variables
                        for k in range(len(cykMatrix[i-1][j])): # k and j are used to iterate over each value in the box
                            for l in range(len(cykMatrix[i-2][j+2])):
                                if cykMatrix[i-1][j][k] == rule[1] and cykMatrix[i-2][j+2][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
                        for k in range(len(cykMatrix[i-2][j])):
                            for l in range(len(cykMatrix[i-1][j+1])):
                                if cykMatrix[i-2][j][k] == rule[1] and cykMatrix[i-1][j+1][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
    return cykMatrix

main()
