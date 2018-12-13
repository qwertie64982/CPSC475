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

# main driver function
def main():
    # get the "dictionary" of grammar rules from file
    # this is actually a list but acts somewhat like a dictionary by attributing variables with variables/terminals
    grammarDict = getGrammar()
    '''
    for line in grammarDict:
        print line
    print
    '''
    
    # get the sentence from file
    sentence = getSentence()
    '''
    print sentence
    print
    '''

    n = len(sentence) # length of sentence, size of matrix (nxn)
    
    # CYK tree represented as an upper triangular matrix
    cykMatrix = [[0 for word in sentence] for word in sentence] # make nxn array
    cykMatrix = removeTriangle(cykMatrix, n) # put null characters where there shouldn't be anything
    cykMatrix = fillMatrix(cykMatrix, n, sentence, grammarDict)
    '''
    for line in cykMatrix:
        print line
    '''
    
    # if there's an S in the final square, then the sentence can be created using this grammar
    # this algorithm constructs the tree bottom-up,
    # so the variables in each level can create whatever is below them
    # thus, if S is at the root, then the utterance can be created from the start variable
    outputValue = False
    for value in cykMatrix[n-1][0]:
        if value == "S":
            outputValue = True
            break
    if outputValue:
        print("Yes")
    else:
        print("No")

# gets the grammar rules from file (argument 1)
# this file is expected to be a CSV with each line representing one rule
# all rules are in Chomsky Normal Form, and "|" operators are split onto separate lines
# thus, if a row has 2 items, it is a terminal (ex. A -> a)
# and if a row has 3 items, it instead has to variables (Ex. S -> AB)
# these are stored as tuples in grammarDict (a list)
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

# gets the input sentence from file (argument 2)
def getSentence():
    with open(sys.argv[2], mode="r") as infile:
        sentence = infile.readline()
    return sentence.split()

# sets null values to every area of the matrix that should never have a value
# this is not necessary but helpful for debugging
def removeTriangle(cykMatrix, n):
    for i in range(1, n):
        for j in range(n-i, n):
            cykMatrix[i][j] = None
    return cykMatrix

# fills the matrix based on the CYK algorithm
def fillMatrix(cykMatrix, n, sentence, grammarDict):
    for i in range(n): # i and j represent the coordinates of the box in the matrix (row, col)
        # first row, where values are soley based on terminals
        if i == 0:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict: # look through the grammar rules for hits
                    if len(rule) == 2: # (terminal rules only)
                        if sentence[j] == rule[1]:
                            cykMatrix[i][j].append(rule[0])
        # all following rows, where values are based on previous rows (variables)
        elif i > 0:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict: # look through the grammar rules for hits
                    if len(rule) == 3: # (variable rules only)
                        for m in range(i): # how many combinations of previous sections are possible (ex. a + ab vs aa + b)
                            for k in range(len(cykMatrix[i-(m+1)][j])): # k and j are used to iterate over each value in the box
                                for l in range(len(cykMatrix[i-(i-m)][j+(i-m)])):
                                    if cykMatrix[i-(m+1)][j][k] == rule[1] and cykMatrix[i-(i-m)][j+(i-m)][l] == rule[2]:
                                        cykMatrix[i][j].append(rule[0])
        '''
        elif i == 1:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if len(rule) == 3: # looking for variables
                        for k in range(len(cykMatrix[i-1][j])): # k and j are used to iterate over each value in the box
                            for l in range(len(cykMatrix[i-1][j+1])):
                                if cykMatrix[i-1][j][k] == rule[1] and cykMatrix[i-1][j+1][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
        elif i == 2:
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
        elif i == 3:
            for j in range(n-i):
                cykMatrix[i][j] = []
                for rule in grammarDict:
                    if len(rule) == 3: # looking for variables
                        for k in range(len(cykMatrix[i-1][j])): # k and j are used to iterate over each value in the box
                            for l in range(len(cykMatrix[i-3][j+3])):
                                if cykMatrix[i-1][j][k] == rule[1] and cykMatrix[i-3][j+3][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
                        for k in range(len(cykMatrix[i-2][j])):
                            for l in range(len(cykMatrix[i-2][j+2])):
                                if cykMatrix[i-2][j][k] == rule[1] and cykMatrix[i-2][j+2][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
                        for k in range(len(cykMatrix[i-3][j])):
                            for l in range(len(cykMatrix[i-1][j+1])):
                                if cykMatrix[i-3][j][k] == rule[1] and cykMatrix[i-1][j+1][l] == rule[2]:
                                    cykMatrix[i][j].append(rule[0])
        '''

    return cykMatrix

main()
